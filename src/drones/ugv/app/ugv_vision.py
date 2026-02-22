import cv2
import time
import os
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration
RTSP_URL = os.environ.get('RTSP_URI', 'rtsp://localhost:8554/cam')
CAMERA_DEVICE = int(os.environ.get("CAMERA_DEVICE", "0"))
MQTT_BROKER = os.environ.get('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_USER = os.environ.get('MQTT_USER', '')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '')
MQTT_TOPIC_DETECTIONS = "ugv/vision/detections"
MQTT_TOPIC_VISION_HEALTH = "ugv/vision/health"

# Simulate Object Detection (Replace with YOLOv8/TFLite inference)
def run_inference(frame):
    # Placeholder: In a real implementation, you would:
    # results = model(frame)
    # detections = results[0].boxes...
    
    # Mock detection for testing
    import random
    detections = []
    if random.random() < 0.1: # 10% chance to detect something
        detections.append({
            "label": "person",
            "confidence": 0.85,
            "bbox": [100, 100, 200, 300]
        })
    return detections

def main():
    print("UGV Vision Pipeline Starting...")
    
    # MQTT Setup
    client = mqtt.Client()
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"Error connecting to MQTT: {e}")
        return

    # Camera Setup:
    # 1) try RTSP first (production path via mediamtx),
    # 2) fallback to local device.
    def open_capture():
        for source in (RTSP_URL, CAMERA_DEVICE):
            cap = cv2.VideoCapture(source)
            if cap.isOpened():
                print(f"Vision source connected: {source}")
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
        print("Cannot open any camera source")
        client.publish(
            MQTT_TOPIC_VISION_HEALTH,
            json.dumps({"status": "camera_unavailable", "timestamp": datetime.now().isoformat()}),
        )
        return

    last_process_time = 0
    PROCESS_INTERVAL = 0.2 # 5 FPS processing to save CPU
    retries = 0
    max_retries_before_reopen = 10

    while True:
        ret, frame = cap.read()
        if not ret:
            retries += 1
            if retries >= max_retries_before_reopen:
                print("Camera read failed repeatedly. Reopening capture...")
                cap.release()
                time.sleep(2)
                cap, current_source = open_capture()
                if cap is None:
                    client.publish(
                        MQTT_TOPIC_VISION_HEALTH,
                        json.dumps(
                            {"status": "camera_unavailable", "timestamp": datetime.now().isoformat()}
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
            time.sleep(0.5)
            continue
        retries = 0

        now = time.time()
        if now - last_process_time > PROCESS_INTERVAL:
            last_process_time = now
            
            # Inference
            detections = run_inference(frame)
            
            if detections:
                payload = {
                    "timestamp": datetime.now().isoformat(),
                    "detections": detections,
                    "count": len(detections)
                }
                client.publish(MQTT_TOPIC_DETECTIONS, json.dumps(payload))
                print(f"Published detection: {detections[0]['label']}")

        # Optional: Add overlay if displaying locally (headless usually doesn't need this)
        # cv2.imshow('UGV Vision', frame)
        # if cv2.waitKey(1) == ord('q'):
        #     break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
