import time
import os
import json
import sys
import math
import hmac
import hashlib
import paho.mqtt.client as mqtt

# Add common folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../common'))
try:
    from defense_controller import DefenseController
except ImportError:
    # Mock defense for now if not found
    class DefenseController:
        def __init__(self, **kwargs): pass
        def get_status(self): return {"state": "mock"}

# Configuration
MQTT_BROKER = os.environ.get('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_USER = os.environ.get('MQTT_USER', '')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '')
DEFENSE_PIN = os.environ.get("DEFENSE_PIN_UAV", "").strip()
if not DEFENSE_PIN:
    raise RuntimeError("DEFENSE_PIN_UAV env var is required for UAV bridge.")
COMMAND_HMAC_SECRET = os.environ.get("COMMAND_HMAC_SECRET_UAV", "").strip()
if not COMMAND_HMAC_SECRET:
    raise RuntimeError("COMMAND_HMAC_SECRET_UAV env var is required for UAV bridge.")
COMMAND_ALLOWED_SOURCES = {
    source.strip() for source in os.environ.get(
        "COMMAND_ALLOWED_SOURCES_UAV", "dashboard,homeassistant"
    ).split(",") if source.strip()
}
COMMAND_MAX_SKEW_SECONDS = int(os.environ.get("COMMAND_MAX_SKEW_SECONDS_UAV", "30"))

MAVLINK_CONNECTION = os.environ.get('MAVLINK_CONNECTION', 'udpin:0.0.0.0:14550')

# Topics
MQTT_TOPIC_STATUS = "uav/status"
MQTT_TOPIC_LOCATION = "uav/location"
MQTT_TOPIC_CMD = "uav/command"

# UAV State (Simulation)
uav_state = {
    "armed": False,
    "mode": "STABILIZE",
    "battery": 100,
    "lat": -23.5505, # Example coordinates
    "lon": -46.6333,
    "alt": 0.0,
    "heading": 0
}

defense = DefenseController(pin_code=DEFENSE_PIN)

# MAVLink Mock (Replacing pymavlink for this MVP script to avoid heavy deps if not needed yet)
# In a real scenario, we would import pymavlink.mavutil and connect.
# Here we simulate the physics loop.

def update_simulated_physics():
    global uav_state
    
    if uav_state["armed"]:
        # Consume battery
        uav_state["battery"] = max(0, uav_state["battery"] - 0.05)
        
        # Simulate movement if in mission mode (simple circle)
        if uav_state["mode"] == "AUTO":
            t = time.time()
            uav_state["lat"] += 0.0001 * math.sin(t * 0.1)
            uav_state["lon"] += 0.0001 * math.cos(t * 0.1)
            uav_state["alt"] = 15.0 + math.sin(t * 0.5)
            uav_state["heading"] = (uav_state["heading"] + 1) % 360

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker (RC: {rc})")
    client.subscribe(MQTT_TOPIC_CMD)

def verify_command_auth(payload):
    source_id = payload.get("source_id")
    timestamp = payload.get("timestamp")
    signature = payload.get("signature")

    if source_id not in COMMAND_ALLOWED_SOURCES:
        return False, f"unauthorized source_id: {source_id}"

    try:
        ts = int(timestamp)
    except (TypeError, ValueError):
        return False, "invalid timestamp"

    if abs(int(time.time()) - ts) > COMMAND_MAX_SKEW_SECONDS:
        return False, "stale command timestamp"

    if not isinstance(signature, str) or not signature:
        return False, "missing signature"

    signed_payload = {k: v for k, v in payload.items() if k != "signature"}
    canonical = json.dumps(signed_payload, sort_keys=True, separators=(",", ":")).encode()
    expected = hmac.new(
        COMMAND_HMAC_SECRET.encode(), canonical, hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        return False, "invalid signature"

    return True, "ok"

def on_message(client, userdata, msg):
    global uav_state
    try:
        payload = json.loads(msg.payload.decode())
        cmd = payload.get('cmd')
        print(f"MQTT CMD: topic={msg.topic} cmd={cmd}")

        authorized, auth_reason = verify_command_auth(payload)
        if not authorized:
            print(f"Ignoring unauthorized command: {auth_reason}")
            return
        
        if cmd == 'arm':
            print("Command: ARM")
            uav_state["armed"] = True
            
        elif cmd == 'disarm':
            print("Command: DISARM")
            uav_state["armed"] = False
            
        elif cmd == 'takeoff':
            print("Command: TAKEOFF")
            uav_state["mode"] = "AUTO"
            uav_state["alt"] = 10.0
            
        elif cmd == 'land':
            print("Command: LAND")
            uav_state["mode"] = "LAND"
            uav_state["alt"] = 0.0
            
    except Exception as e:
        print(f"Error executing command: {e}")

def main():
    print(f"Starting UAV MAVLink Bridge (Simulated Connection: {MAVLINK_CONNECTION})...")
    
    client = mqtt.Client()
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
    except Exception as e:
        print(f"Error connecting to MQTT: {e}")
        return

    last_pub_time = 0
    
    while True:
        update_simulated_physics()
        
        if time.time() - last_pub_time > 1.0:
            # Publish Status
            status = {
                "timestamp": time.time(),
                "armed": uav_state["armed"],
                "mode": uav_state["mode"],
                "battery": round(uav_state["battery"], 1),
                "heading": int(uav_state["heading"])
            }
            client.publish(MQTT_TOPIC_STATUS, json.dumps(status))
            
            # Publish Location (Device Tracker compatible)
            location = {
                "latitude": uav_state["lat"],
                "longitude": uav_state["lon"],
                "altitude": round(uav_state["alt"], 1),
                "gps_accuracy": 2.5
            }
            # For Home Assistant device_tracker.mqtt, usually sends raw payload or specific JSON
            client.publish(MQTT_TOPIC_LOCATION, json.dumps(location))
            
            last_pub_time = time.time()
            
        time.sleep(0.1)

if __name__ == "__main__":
    main()
