import cv2
import time
import os
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration
RTSP_URL = os.environ.get('RTSP_URI', 'rtsp://localhost:8554/cam')
MQTT_BROKER = os.environ.get('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_USER = os.environ.get('MQTT_USER', '')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '')
MQTT_TOPIC_DETECTIONS = "ugv/vision/detections"

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

    # Camera Setup (simulate reading from /dev/video0 if RTSP fails, or just use 0)
    # In production with mediamtx, we might push TO mediamtx via ffmpeg, 
    # and read FROM /dev/video0 here.
    cap = cv2.VideoCapture(0) # Open local camera
    
    if not cap.isOpened():
        print("Cannot open camera")
        return

    last_process_time = 0
    PROCESS_INTERVAL = 0.2 # 5 FPS processing to save CPU

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            time.sleep(1)
            continue

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
