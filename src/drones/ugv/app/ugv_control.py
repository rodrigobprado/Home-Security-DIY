import time
import os
import serial
import json
import sys
import hmac
import hashlib
import shutil
import subprocess
from pathlib import Path
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
ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS = (
    os.environ.get("ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_UGV", "false").strip().lower()
    in {"1", "true", "yes"}
)

MQTT_TOPIC_CMD = "ugv/command"
MQTT_TOPIC_STATUS = "ugv/status"
MQTT_TOPIC_DEFENSE_STATUS = "ugv/defense/status"
MQTT_TOPIC_WAYPOINTS_SET = "ugv/patrol/waypoints/set"
MQTT_TOPIC_WAYPOINTS_STATE = "ugv/patrol/waypoints/state"
MQTT_TOPIC_PATROL_WAYPOINTS = "ugv/patrol/waypoints"
MQTT_TOPIC_LINK_METRICS = "ugv/link/metrics"
MQTT_TOPIC_LORA_CMD = "ugv/lora/command"
MQTT_TOPIC_LINK_STATE = "ugv/link/state"
MQTT_TOPIC_VISION_SAFETY = "ugv/vision/safety"
MQTT_TOPIC_DEFENSE_AUDIT = "ugv/defense/audit"
DEFENSE_PIN = os.environ.get("DEFENSE_PIN_UGV", "").strip()
if not DEFENSE_PIN:
    raise RuntimeError("DEFENSE_PIN_UGV env var is required for UGV control.")
DEFENSE_TOTP_SECRET = os.environ.get("DEFENSE_TOTP_SECRET_UGV", "").strip()
DEFENSE_WARNING_SECONDS = int(os.environ.get("DEFENSE_WARNING_SECONDS_UGV", "5"))
DEFENSE_COOLDOWN_SECONDS = int(os.environ.get("DEFENSE_COOLDOWN_SECONDS_UGV", "30"))
DEFENSE_MAX_TRIGGERS_PER_DAY = int(os.environ.get("DEFENSE_MAX_TRIGGERS_PER_DAY_UGV", "3"))
DEFENSE_EXCLUSION_ZONES = {
    z.strip().lower()
    for z in os.environ.get(
        "DEFENSE_EXCLUSION_ZONES_UGV", "sidewalk,service_entry,neighbor_gate"
    ).split(",")
    if z.strip()
}
DEFENSE_AUDIT_LOG_PATH = os.environ.get(
    "DEFENSE_AUDIT_LOG_PATH_UGV", "/tmp/ugv_defense_audit.log"
).strip()
DEFENSE_ACTUATOR_SPEC = os.environ.get(
    "DEFENSE_ACTUATOR_SPEC_UGV", "solenoid_12v_nc+co2_valve"
).strip()
ROS2_PATROL_TOPIC = os.environ.get("ROS2_PATROL_TOPIC", "/ugv/patrol/goal")
ROS2_ENABLED = os.environ.get("ROS2_ENABLED", "true").strip().lower() in {"1", "true", "yes"}
ROS2_PATROL_ROUTE_FILE = os.environ.get(
    "ROS2_PATROL_ROUTE_FILE", "/app/ros2/routes/patrol_routes.json"
)
WIFI_RSSI_THRESHOLD = int(os.environ.get("WIFI_RSSI_THRESHOLD_UGV", "-78"))
FAILOVER_TIMEOUT_SECONDS = int(os.environ.get("FAILOVER_TIMEOUT_SECONDS_UGV", "30"))

# Serial Connection
ser = None
health = HealthMonitor()
defense = DefenseController(
    pin_code=DEFENSE_PIN,
    totp_secret=DEFENSE_TOTP_SECRET,
    warning_seconds=DEFENSE_WARNING_SECONDS,
    cooldown_seconds=DEFENSE_COOLDOWN_SECONDS,
    max_triggers_per_day=DEFENSE_MAX_TRIGGERS_PER_DAY,
    exclusion_zones=sorted(DEFENSE_EXCLUSION_ZONES),
    audit_log_path=DEFENSE_AUDIT_LOG_PATH,
)
PATROL_ROUTES = {}
CURRENT_LINK_MODE = "wifi"
LAST_LINK_REASON = "startup"
last_mqtt_rx_ts = time.time()
last_link_rssi = -60
defense_blocked = False
defense_block_reasons = []


def load_patrol_routes():
    global PATROL_ROUTES
    routes_file = Path(ROS2_PATROL_ROUTE_FILE)
    default_routes = {
        "perimeter_day": [
            {"x": 0.0, "y": 0.0, "yaw": 0.0},
            {"x": 2.0, "y": 0.0, "yaw": 0.0},
            {"x": 2.0, "y": 2.0, "yaw": 1.57},
            {"x": 0.0, "y": 2.0, "yaw": 3.14},
        ],
        "garage_to_gate": [
            {"x": 0.0, "y": 0.0, "yaw": 0.0},
            {"x": 1.0, "y": -0.5, "yaw": -0.5},
            {"x": 3.0, "y": -1.0, "yaw": 0.0},
        ],
    }

    if not routes_file.exists():
        PATROL_ROUTES = default_routes
        return

    try:
        data = json.loads(routes_file.read_text(encoding="utf-8"))
        if isinstance(data, dict) and data:
            PATROL_ROUTES = data
        else:
            PATROL_ROUTES = default_routes
    except Exception as exc:
        print(f"Failed to load patrol routes ({routes_file}): {exc}")
        PATROL_ROUTES = default_routes


def save_patrol_routes():
    routes_file = Path(ROS2_PATROL_ROUTE_FILE)
    try:
        routes_file.parent.mkdir(parents=True, exist_ok=True)
        routes_file.write_text(
            json.dumps(PATROL_ROUTES, ensure_ascii=True, indent=2),
            encoding="utf-8",
        )
    except Exception as exc:
        print(f"Failed to persist patrol routes: {exc}")


def publish_status(client, payload):
    client.publish(MQTT_TOPIC_STATUS, json.dumps(payload))


def publish_patrol_route(client, route_name, waypoints):
    client.publish(
        MQTT_TOPIC_PATROL_WAYPOINTS,
        json.dumps(
            {
                "route": route_name,
                "waypoint_count": len(waypoints),
                "waypoints": waypoints,
                "ts": int(time.time()),
            }
        ),
    )


def send_route_to_ros2(route_name, waypoints):
    if not ROS2_ENABLED:
        return False, "ros2_disabled"
    if not shutil.which("ros2"):
        return False, "ros2_cli_not_found"

    payload = json.dumps({"route": route_name, "waypoints": waypoints}, ensure_ascii=True)
    cmd = [
        "ros2",
        "topic",
        "pub",
        "--once",
        ROS2_PATROL_TOPIC,
        "std_msgs/msg/String",
        f'{{data: "{payload.replace(chr(34), chr(92) + chr(34))}"}}',
    ]

    try:
        proc = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        stdout = (proc.stdout or "").strip()
        if stdout:
            print(f"ROS2 patrol publish output: {stdout}")
        return True, "published_to_ros2"
    except Exception as exc:
        return False, str(exc)

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT Broker with result code {rc}")
    client.subscribe(MQTT_TOPIC_CMD)
    client.subscribe(MQTT_TOPIC_WAYPOINTS_SET)
    client.subscribe(MQTT_TOPIC_LINK_METRICS)
    client.subscribe(MQTT_TOPIC_LORA_CMD)
    client.subscribe(MQTT_TOPIC_VISION_SAFETY)


def on_disconnect(client, userdata, rc):
    print(f"Disconnected from MQTT Broker rc={rc}")


def set_link_mode(client, mode, reason):
    global CURRENT_LINK_MODE, LAST_LINK_REASON
    if mode == CURRENT_LINK_MODE and reason == LAST_LINK_REASON:
        return
    CURRENT_LINK_MODE = mode
    LAST_LINK_REASON = reason
    try:
        client.publish(
            MQTT_TOPIC_LINK_STATE,
            json.dumps(
                {
                    "mode": CURRENT_LINK_MODE,
                    "reason": LAST_LINK_REASON,
                    "ts": int(time.time()),
                    "rssi": last_link_rssi,
                }
            ),
        )
    except Exception as exc:
        print(f"Failed to publish link mode: {exc}")


def handle_lora_command(client, payload):
    cmd = str(payload.get("cmd", "")).strip().upper()
    if cmd == "STOP":
        send_motor_cmd(0, 0)
        publish_status(
            client,
            {
                "state": "emergency_stop",
                "command": "lora_stop",
                "status": "executed",
            },
        )
    elif cmd == "RTH":
        route_name = "garage_to_gate"
        waypoints = PATROL_ROUTES.get(route_name, [])
        if waypoints:
            publish_patrol_route(client, route_name, waypoints)
            publish_status(
                client,
                {
                    "state": "patrol",
                    "command": "lora_rth",
                    "status": "started_mqtt_only",
                    "route": route_name,
                },
            )
    elif cmd == "ALARM":
        publish_status(
            client,
            {
                "state": "alert",
                "command": "lora_alarm",
                "status": "forwarded",
            },
        )

def verify_command_auth(payload):
    source_id = payload.get("source_id")
    timestamp = payload.get("timestamp")
    signature = payload.get("signature")

    if source_id not in COMMAND_ALLOWED_SOURCES:
        return False, f"unauthorized source_id: {source_id}"

    if ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS and source_id == "homeassistant":
        if not isinstance(signature, str) or not signature:
            return True, "unsigned_homeassistant_allowed"

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
    global last_mqtt_rx_ts, last_link_rssi, defense_blocked, defense_block_reasons
    try:
        health.update_heartbeat()
        payload = json.loads(msg.payload.decode())
        command = payload.get("cmd")
        print(f"MQTT CMD: topic={msg.topic} cmd={command}")
        last_mqtt_rx_ts = time.time()

        if msg.topic == MQTT_TOPIC_LINK_METRICS:
            rssi = payload.get("wifi_rssi")
            try:
                last_link_rssi = int(rssi)
            except (TypeError, ValueError):
                pass
            return

        if msg.topic == MQTT_TOPIC_VISION_SAFETY:
            defense_blocked = bool(payload.get("defense_blocked", False))
            raw_reasons = payload.get("reasons")
            defense_block_reasons = raw_reasons if isinstance(raw_reasons, list) else []
            return

        authorized, auth_reason = verify_command_auth(payload)
        if not authorized:
            print(f"Ignoring unauthorized command: {auth_reason}")
            return

        if msg.topic == MQTT_TOPIC_WAYPOINTS_SET:
            route_name = str(payload.get("route", "")).strip()
            waypoints = payload.get("waypoints")
            if not route_name or not isinstance(waypoints, list) or not waypoints:
                client.publish(
                    MQTT_TOPIC_WAYPOINTS_STATE,
                    json.dumps(
                        {
                            "status": "invalid_payload",
                            "route": route_name or None,
                            "reason": "route and waypoints list are required",
                        }
                    ),
                )
                return

            PATROL_ROUTES[route_name] = waypoints
            save_patrol_routes()
            client.publish(
                MQTT_TOPIC_WAYPOINTS_STATE,
                json.dumps(
                    {
                        "status": "updated",
                        "route": route_name,
                        "waypoint_count": len(waypoints),
                    }
                ),
            )
            return

        if msg.topic == MQTT_TOPIC_LORA_CMD:
            handle_lora_command(client, payload)
            return

        is_healthy, reason = health.check_health()

        # Defense commands
        if command == "defense_mode":
            ok, detail = defense.set_mode(payload.get("mode", ""))
            client.publish(
                MQTT_TOPIC_DEFENSE_STATUS,
                json.dumps(
                    {
                        **defense.get_status(),
                        "command": "defense_mode",
                        "result": "ok" if ok else "rejected",
                        "detail": detail,
                    }
                ),
            )
            return

        if command == "defense_arm":
            if not is_healthy:
                client.publish(
                    MQTT_TOPIC_DEFENSE_STATUS,
                    json.dumps(
                        {
                            **defense.get_status(),
                            "command": "defense_arm",
                            "result": "rejected",
                            "detail": f"health:{reason}",
                        }
                    ),
                )
                return
            ok, detail = defense.arm(
                payload.get("pin", ""),
                payload.get("totp", ""),
                source_id=str(payload.get("source_id", "unknown")),
            )
            client.publish(
                MQTT_TOPIC_DEFENSE_STATUS,
                json.dumps(
                    {
                        **defense.get_status(),
                        "command": "defense_arm",
                        "result": "ok" if ok else "rejected",
                        "detail": detail,
                    }
                ),
            )
            return
        if command == "defense_disarm":
            defense.disarm("request")
            client.publish(
                MQTT_TOPIC_DEFENSE_STATUS,
                json.dumps(
                    {
                        **defense.get_status(),
                        "command": "defense_disarm",
                        "result": "ok",
                    }
                ),
            )
            return
        if command in {"defense_auto_fire", "defense_set_automatic"}:
            client.publish(
                MQTT_TOPIC_DEFENSE_STATUS,
                json.dumps(
                    {
                        **defense.get_status(),
                        "command": command,
                        "result": "rejected",
                        "detail": "automatic_mode_forbidden",
                    }
                ),
            )
            return
        if command == "defense_fire":
            if not is_healthy:
                client.publish(
                    MQTT_TOPIC_DEFENSE_STATUS,
                    json.dumps(
                        {
                            **defense.get_status(),
                            "command": "defense_fire",
                            "result": "rejected",
                            "detail": f"health:{reason}",
                        }
                    ),
                )
                return
            ok, detail = defense.request_fire(
                zone=str(payload.get("zone", "")).strip().lower(),
                defense_blocked=defense_blocked,
                block_reasons=defense_block_reasons,
                source_id=str(payload.get("source_id", "unknown")),
            )
            defense_payload = defense.get_status()
            defense_payload.update(
                {
                    "command": "defense_fire",
                    "result": "ok" if ok else "pending_or_rejected",
                    "detail": detail,
                    "vision_blocked": defense_blocked,
                    "vision_reasons": defense_block_reasons,
                }
            )
            client.publish(MQTT_TOPIC_DEFENSE_STATUS, json.dumps(defense_payload))
            client.publish(
                MQTT_TOPIC_DEFENSE_AUDIT,
                json.dumps(
                    {
                        "ts": int(time.time()),
                        "event": "defense_fire_attempt",
                        "result": detail,
                        "zone": str(payload.get("zone", "")).strip().lower() or None,
                        "source_id": str(payload.get("source_id", "unknown")),
                    }
                ),
            )
            return

        # Nav Commands (Only if Healthy)
        if not is_healthy:
            print(f"Ignoring command due to health failure: {reason}")
            return

        if command == "move":
            left = int(payload.get("linear", 0) * 100)
            right = int(payload.get("angular", 0) * 100)
            send_motor_cmd(left, right)
        elif command == "stop":
            send_motor_cmd(0, 0)
            publish_status(
                client,
                {
                    "state": "idle",
                    "command": "stop",
                    "status": "executed",
                },
            )
        elif command == "return_home":
            route_name = "garage_to_gate"
            waypoints = PATROL_ROUTES.get(route_name, [])
            if not waypoints:
                publish_status(
                    client,
                    {
                        "state": "error",
                        "command": "return_home",
                        "status": "route_not_found",
                    },
                )
                return
            publish_patrol_route(client, route_name, waypoints)
            publish_status(
                client,
                {
                    "state": "patrol",
                    "command": "return_home",
                    "status": "started_mqtt_only",
                    "route": route_name,
                },
            )
        elif command == 'patrol':
            route_name = str(payload.get("route", "perimeter_day")).strip() or "perimeter_day"
            waypoints = payload.get("waypoints")
            if not isinstance(waypoints, list) or not waypoints:
                waypoints = PATROL_ROUTES.get(route_name)

            if not waypoints:
                publish_status(
                    client,
                    {
                        "state": "error",
                        "command": "patrol",
                        "status": "route_not_found",
                        "route": route_name,
                        "known_routes": sorted(PATROL_ROUTES.keys()),
                    },
                )
                return

            publish_patrol_route(client, route_name, waypoints)
            ros2_ok, ros2_reason = send_route_to_ros2(route_name, waypoints)
            publish_status(
                client,
                {
                    "state": "patrol",
                    "command": "patrol",
                    "status": "started" if ros2_ok else "started_mqtt_only",
                    "route": route_name,
                    "waypoint_count": len(waypoints),
                    "ros2": {"sent": ros2_ok, "detail": ros2_reason},
                },
            )

    except Exception as e:
        print(f"Error parsing command: {e}")

def send_motor_cmd(left, right):
    if ser and ser.is_open:
        cmd = f"M {left} {right}\n"
        ser.write(cmd.encode())
        print(f"Sent to ESP32: {cmd.strip()}")

def main():
    global ser, last_mqtt_rx_ts
    print("UGV Brain Starting...")
    load_patrol_routes()
    
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
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        health.update_heartbeat()
        client.loop_start()
        last_mqtt_rx_ts = time.time()
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
            stale = (time.time() - last_mqtt_rx_ts) > FAILOVER_TIMEOUT_SECONDS
            if stale or last_link_rssi < WIFI_RSSI_THRESHOLD:
                set_link_mode(client, "lora", "wifi_timeout_or_low_rssi")
            else:
                set_link_mode(client, "wifi", "wifi_healthy")
            
            # UGV Status
            status = {
                "state": "idle" if is_healthy else "error",
                "health_reason": reason,
                "battery": health.battery_level,
                "odometry": {"left": ticks_l, "right": ticks_r},
                "comm": {
                    "mode": CURRENT_LINK_MODE,
                    "reason": LAST_LINK_REASON,
                    "wifi_rssi": last_link_rssi,
                    "failover_timeout_s": FAILOVER_TIMEOUT_SECONDS,
                },
            }
            client.publish(MQTT_TOPIC_STATUS, json.dumps(status))
            
            # Defense Status
            defense_status = defense.get_status()
            defense_status.update(
                {
                    "actuator_spec": DEFENSE_ACTUATOR_SPEC,
                    "vision_blocked": defense_blocked,
                    "vision_reasons": defense_block_reasons,
                }
            )
            client.publish(MQTT_TOPIC_DEFENSE_STATUS, json.dumps(defense_status))
            
            last_pub_time = time.time()
        
        time.sleep(0.01)

if __name__ == "__main__":
    main()
