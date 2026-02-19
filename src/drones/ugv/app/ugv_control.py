import time
import os
import serial
import json
import sys
import hmac
import hashlib
import paho.mqtt.client as mqtt

# Add common folder to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
try:
    from health_monitor import HealthMonitor
    from defense_controller import DefenseController
except ImportError as e:
    print(f"Error importing common modules: {e}")
    # Mock for testing if modules missing
    class HealthMonitor:
        def __init__(self, **kwargs): pass
        def check_health(self): return True, "OK"
        def update_heartbeat(self): pass
    class DefenseController:
        def __init__(self, **kwargs): pass
        def get_status(self): return {"state": "mock"}

# Configuration from Environment Variables
SERIAL_PORT = os.environ.get('SERIAL_PORT', '/dev/ttyUSB0')
BAUD_RATE = int(os.environ.get('BAUD_RATE', 115200))

MQTT_BROKER = os.environ.get('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.environ.get('MQTT_PORT', 1883))
MQTT_USER = os.environ.get('MQTT_USER', '')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '')
COMMAND_HMAC_SECRET = os.environ.get("COMMAND_HMAC_SECRET_UGV", "").strip()
if not COMMAND_HMAC_SECRET:
    raise RuntimeError("COMMAND_HMAC_SECRET_UGV env var is required for UGV control.")
COMMAND_ALLOWED_SOURCES = {
    source.strip() for source in os.environ.get(
        "COMMAND_ALLOWED_SOURCES_UGV", "dashboard,homeassistant"
    ).split(",") if source.strip()
}
COMMAND_MAX_SKEW_SECONDS = int(os.environ.get("COMMAND_MAX_SKEW_SECONDS_UGV", "30"))

MQTT_TOPIC_CMD = "ugv/command"
MQTT_TOPIC_STATUS = "ugv/status"
MQTT_TOPIC_DEFENSE_STATUS = "ugv/defense/status"
DEFENSE_PIN = os.environ.get("DEFENSE_PIN_UGV", "").strip()
if not DEFENSE_PIN:
    raise RuntimeError("DEFENSE_PIN_UGV env var is required for UGV control.")

# Serial Connection
ser = None
health = HealthMonitor()
defense = DefenseController(pin_code=DEFENSE_PIN)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
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
    try:
        health.update_heartbeat()
        payload = json.loads(msg.payload.decode())
        command = payload.get('cmd')
        print(f"MQTT CMD: topic={msg.topic} cmd={command}")

        authorized, auth_reason = verify_command_auth(payload)
        if not authorized:
            print(f"Ignoring unauthorized command: {auth_reason}")
            return

        is_healthy, reason = health.check_health()

        # Defense Commands
        if command == 'defense_arm':
            if not is_healthy:
                print(f"Blocking defense_arm due to health failure: {reason}")
                return
            defense.arm(payload.get('pin', ''))
            return
        elif command == 'defense_disarm':
            defense.disarm("Request")
            return

        # Nav Commands (Only if Healthy)
        if not is_healthy:
            print(f"Ignoring command due to health failure: {reason}")
            return

        if command == 'move':
            left = int(payload.get('linear', 0) * 100)
            right = int(payload.get('angular', 0) * 100)
            send_motor_cmd(left, right)
            
        elif command == 'patrol':
            print("Patrol command received but feature is not implemented yet.")
            client.publish(
                MQTT_TOPIC_STATUS,
                json.dumps(
                    {
                        "state": "warning",
                        "command": "patrol",
                        "status": "not_implemented",
                        "reason": "Patrol sequence pending implementation",
                    }
                ),
            )
            
    except Exception as e:
        print(f"Error parsing command: {e}")

def send_motor_cmd(left, right):
    if ser and ser.is_open:
        cmd = f"M {left} {right}\n"
        ser.write(cmd.encode())
        print(f"Sent to ESP32: {cmd.strip()}")

def main():
    global ser
    print("UGV Brain Starting...")
    
    # 1. Connect to ESP32
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
        print(f"Connected to ESP32 on {SERIAL_PORT}")
    except Exception as e:
        print(f"Error connecting to ESP32: {e}")
    
    # 2. Connect to MQTT
    client = mqtt.Client()
    if MQTT_USER and MQTT_PASSWORD:
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        health.update_heartbeat()
        client.loop_start()
    except Exception as e:
        print(f"Error connecting to MQTT: {e}")
        return

    # 3. Main Loop
    last_pub_time = 0
    ticks_l = 0
    ticks_r = 0
    
    while True:
        # Check Health
        is_healthy, reason = health.check_health()
        if not is_healthy:
            # Emergency Stop
            if ser and ser.is_open:
                 # Only send stop if we haven't sent it recently/repeatedly to avoid flooding
                 pass # simplified
            # print(f"CRITICAL HEALTH: {reason}")
        
        # Read ESP32
        if ser and ser.is_open and ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                health.update_heartbeat() # Serial activity counts as heartbeat too? No, comms check.
                
                if line.startswith("O "):
                    parts = line.split()
                    if len(parts) == 3:
                        ticks_l = int(parts[1])
                        ticks_r = int(parts[2])
                elif line.startswith("B "):
                    parts = line.split()
                    if len(parts) == 2:
                        try:
                            battery_level = int(parts[1])
                            health.update_battery(max(0, min(100, battery_level)))
                        except ValueError:
                            print(f"Invalid battery payload: {line}")
                elif line.startswith("LoRa Recv: "):
                    print(f"[LoRa] {line.strip()}")
            except Exception as e:
                print(f"Serial Read Error: {e}")

        # Publish Telemetry (1Hz)
        if time.time() - last_pub_time > 1.0:
            
            # UGV Status
            status = {
                "state": "idle" if is_healthy else "error",
                "health_reason": reason,
                "battery": health.battery_level,
                "odometry": {"left": ticks_l, "right": ticks_r}
            }
            client.publish(MQTT_TOPIC_STATUS, json.dumps(status))
            
            # Defense Status
            client.publish(MQTT_TOPIC_DEFENSE_STATUS, json.dumps(defense.get_status()))
            
            last_pub_time = time.time()
        
        time.sleep(0.01)

if __name__ == "__main__":
    main()
