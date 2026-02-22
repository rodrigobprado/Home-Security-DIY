import json
import os
import time
import sys
from pathlib import Path
from datetime import datetime

import cv2
import paho.mqtt.client as mqtt

# Reuse same detection strategy as UGV, but with UAV topics.
sys.path.append(str(Path(__file__).resolve().parents[1] / "ugv" / "app"))
from ugv_vision import (
    SortLikeTracker,
    YoloV8Backend,
    TFLiteBackend,
    annotate_safety,
)

RTSP_URL = os.environ.get("UAV_RTSP_URI", "rtsp://localhost:8554/uav")
CAMERA_DEVICE = int(os.environ.get("UAV_CAMERA_DEVICE", "0"))
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_USER = os.environ.get("MQTT_USER", "")
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD", "")

MODEL_BACKEND = os.environ.get("UAV_VISION_BACKEND", "yolov8")
YOLO_MODEL_PATH = os.environ.get("UAV_YOLO_MODEL_PATH", "/app/models/yolov8n.pt")
TFLITE_MODEL_PATH = os.environ.get("UAV_TFLITE_MODEL_PATH", "/app/models/yolov8n_int8.tflite")
TFLITE_LABELS_PATH = os.environ.get("UAV_TFLITE_LABELS_PATH", "/app/models/coco_labels.txt")
VISION_MIN_CONF = float(os.environ.get("UAV_VISION_MIN_CONF", "0.35"))
PROCESS_FPS = float(os.environ.get("UAV_VISION_PROCESS_FPS", "6.0"))

MQTT_TOPIC_DETECTIONS = "uav/vision/detections"
MQTT_TOPIC_HEALTH = "uav/vision/health"
MQTT_TOPIC_SAFETY = "uav/vision/safety"


def create_backend():
    if MODEL_BACKEND == "tflite":
        return TFLiteBackend(TFLITE_MODEL_PATH, TFLITE_LABELS_PATH, VISION_MIN_CONF)
    return YoloV8Backend(YOLO_MODEL_PATH, VISION_MIN_CONF)


def main():
    client = mqtt.Client()
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()

    backend = create_backend()
    tracker = SortLikeTracker(max_disappeared=12, max_distance=120)

    def open_capture():
        for source in (RTSP_URL, CAMERA_DEVICE):
            cap = cv2.VideoCapture(source)
            if cap.isOpened():
                client.publish(
                    MQTT_TOPIC_HEALTH,
                    json.dumps(
                        {
                            "status": "camera_connected",
                            "source": str(source),
                            "backend": MODEL_BACKEND,
                            "timestamp": datetime.now().isoformat(),
                        }
                    ),
                )
                return cap, source
        return None, None

    cap, source = open_capture()
    if cap is None:
        client.publish(
            MQTT_TOPIC_HEALTH,
            json.dumps({"status": "camera_unavailable", "timestamp": datetime.now().isoformat()}),
        )
        return

    interval = 1.0 / max(1.0, PROCESS_FPS)
    last = 0.0

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            time.sleep(1.0)
            cap, source = open_capture()
            if cap is None:
                time.sleep(5.0)
            continue

        now = time.time()
        if now - last < interval:
            continue
        last = now

        detections = backend.infer(frame)
        tracked = tracker.update(detections)
        block_defense = annotate_safety(tracked, frame.shape)

        client.publish(
            MQTT_TOPIC_DETECTIONS,
            json.dumps(
                {
                    "timestamp": datetime.now().isoformat(),
                    "backend": MODEL_BACKEND,
                    "source": str(source),
                    "count": len(tracked),
                    "detections": tracked,
                    "defense_blocked": block_defense,
                }
            ),
        )

        client.publish(
            MQTT_TOPIC_SAFETY,
            json.dumps(
                {
                    "timestamp": datetime.now().isoformat(),
                    "defense_blocked": block_defense,
                }
            ),
        )


if __name__ == "__main__":
    main()
