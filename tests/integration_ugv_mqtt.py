import time
import json
import hmac
import hashlib
import os
import paho.mqtt.client as mqtt
import sys

# Configuration (Mock HA)
MQTT_BROKER = "localhost" # Assumes Mosquitto is running via Docker
MQTT_PORT = 1883
MQTT_USER = "homeassistant"
MQTT_PASSWORD = "CHANGE_ME"
COMMAND_HMAC_SECRET = os.environ.get("COMMAND_HMAC_SECRET_UGV", "CHANGE_ME_ugv_hmac_secret")
SOURCE_ID = os.environ.get("COMMAND_SOURCE_ID", "homeassistant")

TOPIC_STATUS = "ugv/status"
TOPIC_CMD = "ugv/command"
TOPIC_DETECTIONS = "ugv/vision/detections"

# Test State
received_status = False
received_detection = False
current_ugv_state = None

def on_connect(client, userdata, flags, rc):
    print(f"Connected to Broker (RC: {rc})")
    client.subscribe(TOPIC_STATUS)
    client.subscribe(TOPIC_DETECTIONS)

def on_message(client, userdata, msg):
    global received_status, received_detection, current_ugv_state
    
    try:
        payload = json.loads(msg.payload.decode())
        
        if msg.topic == TOPIC_STATUS:
            print(f"[STATUS] Battery: {payload.get('battery')}% | State: {payload.get('state')}")
            received_status = True
            current_ugv_state = payload.get('state')
            
        elif msg.topic == TOPIC_DETECTIONS:
            count = payload.get('count', 0)
            print(f"[VISION] Detected {count} objects")
            if count > 0:
                received_detection = True
                
    except Exception as e:
        print(f"Error parsing msg: {e}")

def main():
    print("Starting UGV Integration Test (Mock HA)...")
    
    client = mqtt.Client(client_id="test_runner")
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")
        print("Ensure Mosquitto container is running: docker compose up -d mosquitto")
        sys.exit(1)

    # 1. Wait for Heartbeat (Status)
    print("Step 1: Waiting for UGV Status...")
    timeout = 10
    start_time = time.time()
    while not received_status and (time.time() - start_time < timeout):
        time.sleep(0.5)
    
    if not received_status:
        print("FAIL: No status received from UGV. Is ugv_control.py running?")
        sys.exit(1)
    print("PASS: Received UGV Status.")

    # 2. Send Command (Move)
    print("Step 2: Sending Move Command...")
    cmd = signed_command({"cmd": "move", "linear": 0.5, "angular": 0.0})
    client.publish(TOPIC_CMD, json.dumps(cmd))
    time.sleep(1) # Wait for processing

    # 3. Send Patrol Command
    print("Step 3: Sending Patrol Command...")
    cmd = signed_command({"cmd": "patrol"})
    client.publish(TOPIC_CMD, json.dumps(cmd))
    time.sleep(1)
    
    # 4. Check Vision (Optional - depends if vision script is sending mock data)
    print("Step 4: Checking Vision Stream (Mock)...")
    timeout = 15 # Wait a bit longer for random mock detection
    start_time = time.time()
    while not received_detection and (time.time() - start_time < timeout):
        time.sleep(0.5)

    if received_detection:
        print("PASS: Received Vision Detections.")
    else:
        print("WARN: No detections received (this is normal if mock random chance didn't trigger).")

    print("\nTEST SUMMARY: SUCCESS")
    print("UGV Controller is responsive to MQTT and publishing telemetry.")
    
    client.loop_stop()
    client.disconnect()

def signed_command(payload: dict) -> dict:
    base = {
        **payload,
        "source_id": SOURCE_ID,
        "timestamp": int(time.time()),
    }
    canonical = json.dumps(base, sort_keys=True, separators=(",", ":")).encode()
    base["signature"] = hmac.new(
        COMMAND_HMAC_SECRET.encode(), canonical, hashlib.sha256
    ).hexdigest()
    return base


if __name__ == "__main__":
    main()
