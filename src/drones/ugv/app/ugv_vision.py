import json
import math
import os
import time
from collections import OrderedDict
from datetime import datetime

import cv2
import paho.mqtt.client as mqtt

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
RTSP_URL = os.environ.get("RTSP_URI", "rtsp://localhost:8554/cam")
CAMERA_DEVICE = int(os.environ.get("CAMERA_DEVICE", "0"))
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_USER = os.environ.get("MQTT_USER", "")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "")

MODEL_BACKEND = os.environ.get("VISION_BACKEND", "yolov8")  # yolov8 | tflite
YOLO_MODEL_PATH = os.environ.get("YOLO_MODEL_PATH", "/app/models/yolov8n.pt")
TFLITE_MODEL_PATH = os.environ.get("TFLITE_MODEL_PATH", "/app/models/yolov8n_int8.tflite")
TFLITE_LABELS_PATH = os.environ.get("TFLITE_LABELS_PATH", "/app/models/coco_labels.txt")
VISION_MIN_CONF = float(os.environ.get("VISION_MIN_CONF", "0.35"))
PROCESS_FPS = float(os.environ.get("VISION_PROCESS_FPS", "6.0"))

MQTT_TOPIC_DETECTIONS = "ugv/vision/detections"
MQTT_TOPIC_VISION_HEALTH = "ugv/vision/health"
MQTT_TOPIC_VISION_METRICS = "ugv/vision/metrics"
MQTT_TOPIC_VISION_SAFETY = "ugv/vision/safety"

TARGET_CLASSES = {"person", "car", "dog"}
ANIMAL_CLASSES = {"dog", "cat"}


# ----------------------------------------------------------------------------
# Tracking (SORT-like centroid tracker)
# ----------------------------------------------------------------------------
class SortLikeTracker:
    def __init__(self, max_disappeared=10, max_distance=90):
        self.next_id = 1
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance

    @staticmethod
    def _centroid(bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def _register(self, detection):
        self.objects[self.next_id] = detection
        self.disappeared[self.next_id] = 0
        self.next_id += 1

    def _deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, detections):
        if len(detections) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self._deregister(object_id)
            return []

        if len(self.objects) == 0:
            for det in detections:
                self._register(det)
            return self._format_tracked()

        object_ids = list(self.objects.keys())
        object_centroids = [self._centroid(self.objects[oid]["bbox"]) for oid in object_ids]
        input_centroids = [self._centroid(det["bbox"]) for det in detections]

        used_rows = set()
        used_cols = set()

        for row, oc in enumerate(object_centroids):
            best_col = None
            best_dist = None
            for col, ic in enumerate(input_centroids):
                if col in used_cols:
                    continue
                dist = math.hypot(oc[0] - ic[0], oc[1] - ic[1])
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    best_col = col
            if best_col is None or best_dist is None or best_dist > self.max_distance:
                continue
            oid = object_ids[row]
            self.objects[oid] = detections[best_col]
            self.disappeared[oid] = 0
            used_rows.add(row)
            used_cols.add(best_col)

        for row, oid in enumerate(object_ids):
            if row in used_rows:
                continue
            self.disappeared[oid] += 1
            if self.disappeared[oid] > self.max_disappeared:
                self._deregister(oid)

        for col, det in enumerate(detections):
            if col in used_cols:
                continue
            self._register(det)

        return self._format_tracked()

    def _format_tracked(self):
        tracked = []
        for oid, det in self.objects.items():
            out = dict(det)
            out["track_id"] = oid
            tracked.append(out)
        return tracked


# ----------------------------------------------------------------------------
# Detection backends
# ----------------------------------------------------------------------------
class VisionBackend:
    def infer(self, frame):
        raise NotImplementedError


class YoloV8Backend(VisionBackend):
    def __init__(self, model_path, min_conf):
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise RuntimeError("ultralytics not installed for YOLOv8 backend") from exc

        self.model = YOLO(model_path)
        self.min_conf = min_conf

    def infer(self, frame):
        results = self.model.predict(frame, verbose=False, conf=self.min_conf)
        detections = []
        for result in results:
            names = result.names
            for box in result.boxes:
                cls_id = int(box.cls[0].item())
                label = names.get(cls_id, str(cls_id)).lower()
                if label not in TARGET_CLASSES and label not in ANIMAL_CLASSES:
                    continue
                conf = float(box.conf[0].item())
                x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
                detections.append(
                    {
                        "label": label,
                        "confidence": round(conf, 3),
                        "bbox": [x1, y1, x2, y2],
                        "backend": "yolov8",
                    }
                )
        return detections


class TFLiteBackend(VisionBackend):
    def __init__(self, model_path, labels_path, min_conf):
        try:
            from tflite_runtime.interpreter import Interpreter
        except ImportError:
            try:
                from tensorflow.lite.python.interpreter import Interpreter
            except ImportError as exc:
                raise RuntimeError("tflite runtime not available") from exc

        self.interpreter = Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.min_conf = min_conf

        self.labels = {}
        if os.path.exists(labels_path):
            with open(labels_path, "r", encoding="utf-8") as fh:
                for i, line in enumerate(fh):
                    self.labels[i] = line.strip().lower()

    def infer(self, frame):
        # Generic TFLite detection parser (boxes, classes, scores, count).
        inp = self.input_details[0]
        h, w = inp["shape"][1], inp["shape"][2]
        resized = cv2.resize(frame, (w, h))
        tensor = resized.astype("float32")
        tensor = tensor[None, ...]

        self.interpreter.set_tensor(inp["index"], tensor)
        self.interpreter.invoke()

        boxes = self.interpreter.get_tensor(self.output_details[0]["index"])[0]
        classes = self.interpreter.get_tensor(self.output_details[1]["index"])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]["index"])[0]
        count = int(self.interpreter.get_tensor(self.output_details[3]["index"])[0])

        fh, fw = frame.shape[:2]
        detections = []
        for i in range(count):
            score = float(scores[i])
            if score < self.min_conf:
                continue
            cls = int(classes[i])
            label = self.labels.get(cls, str(cls)).lower()
            if label not in TARGET_CLASSES and label not in ANIMAL_CLASSES:
                continue
            y1, x1, y2, x2 = boxes[i]
            detections.append(
                {
                    "label": label,
                    "confidence": round(score, 3),
                    "bbox": [int(x1 * fw), int(y1 * fh), int(x2 * fw), int(y2 * fh)],
                    "backend": "tflite",
                }
            )
        return detections


def create_backend():
    if MODEL_BACKEND == "tflite":
        return TFLiteBackend(TFLITE_MODEL_PATH, TFLITE_LABELS_PATH, VISION_MIN_CONF)
    return YoloV8Backend(YOLO_MODEL_PATH, VISION_MIN_CONF)


def annotate_safety(detections, frame_shape):
    fh, _fw = frame_shape[:2]
    block_defense = False

    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        h = max(1, y2 - y1)
        det["safety_block_reason"] = None

        if det["label"] in ANIMAL_CLASSES:
            det["safety_block_reason"] = "animal_detected"
            block_defense = True
            continue

        # Conservative rule: smaller person bbox can indicate child/distant ambiguity.
        if det["label"] == "person" and (h / max(1, fh)) < 0.35:
            det["safety_block_reason"] = "possible_child_or_uncertain_person"
            block_defense = True

    return block_defense


def main():
    print("UGV Vision Pipeline Starting...")

    client = mqtt.Client()
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as exc:
        print(f"Error connecting to MQTT: {exc}")
        return

    try:
        backend = create_backend()
        client.publish(
            MQTT_TOPIC_VISION_HEALTH,
            json.dumps(
                {
                    "status": "model_loaded",
                    "backend": MODEL_BACKEND,
                    "timestamp": datetime.now().isoformat(),
                }
            ),
        )
    except Exception as exc:
        print(f"Model initialization failed: {exc}")
        client.publish(
            MQTT_TOPIC_VISION_HEALTH,
            json.dumps(
                {
                    "status": "model_error",
                    "error": str(exc),
                    "timestamp": datetime.now().isoformat(),
                }
            ),
        )
        return

    def open_capture():
        for source in (RTSP_URL, CAMERA_DEVICE):
            cap = cv2.VideoCapture(source)
            if cap.isOpened():
                client.publish(
                    MQTT_TOPIC_VISION_HEALTH,
                    json.dumps(
                        {
                            "status": "camera_connected",
                            "source": str(source),
                            "timestamp": datetime.now().isoformat(),
                        }
                    ),
                )
                return cap, source
        return None, None

    cap, current_source = open_capture()
    if cap is None:
        client.publish(
            MQTT_TOPIC_VISION_HEALTH,
            json.dumps({"status": "camera_unavailable", "timestamp": datetime.now().isoformat()}),
        )
        return

    tracker = SortLikeTracker(max_disappeared=15, max_distance=100)
    process_interval = 1.0 / max(1.0, PROCESS_FPS)

    retries = 0
    max_retries_before_reopen = 10
    last_process_time = 0.0
    frame_count = 0
    fps_window_start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            retries += 1
            if retries >= max_retries_before_reopen:
                cap.release()
                time.sleep(2)
                cap, current_source = open_capture()
                if cap is None:
                    client.publish(
                        MQTT_TOPIC_VISION_HEALTH,
                        json.dumps(
                            {
                                "status": "camera_unavailable",
                                "timestamp": datetime.now().isoformat(),
                            }
                        ),
                    )
                    time.sleep(10)
                else:
                    client.publish(
                        MQTT_TOPIC_VISION_HEALTH,
                        json.dumps(
                            {
                                "status": "camera_recovered",
                                "source": str(current_source),
                                "timestamp": datetime.now().isoformat(),
                            }
                        ),
                    )
                retries = 0
            time.sleep(0.2)
            continue

        retries = 0

        now = time.time()
        if now - last_process_time < process_interval:
            continue
        last_process_time = now

        detections = backend.infer(frame)
        tracked = tracker.update(detections)
        block_defense = annotate_safety(tracked, frame.shape)

        payload = {
            "timestamp": datetime.now().isoformat(),
            "backend": MODEL_BACKEND,
            "source": str(current_source),
            "count": len(tracked),
            "detections": tracked,
            "defense_blocked": block_defense,
        }
        client.publish(MQTT_TOPIC_DETECTIONS, json.dumps(payload))

        client.publish(
            MQTT_TOPIC_VISION_SAFETY,
            json.dumps(
                {
                    "timestamp": payload["timestamp"],
                    "defense_blocked": block_defense,
                    "reasons": [d["safety_block_reason"] for d in tracked if d["safety_block_reason"]],
                }
            ),
        )

        frame_count += 1
        elapsed = max(0.001, now - fps_window_start)
        if elapsed >= 5.0:
            fps = frame_count / elapsed
            client.publish(
                MQTT_TOPIC_VISION_METRICS,
                json.dumps(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "fps": round(fps, 2),
                        "target_fps": PROCESS_FPS,
                        "meets_target": fps >= 5.0,
                        "backend": MODEL_BACKEND,
                    }
                ),
            )
            frame_count = 0
            fps_window_start = now


if __name__ == "__main__":
    main()
