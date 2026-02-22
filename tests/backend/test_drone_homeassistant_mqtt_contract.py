from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MQTT_YAML = ROOT / "src" / "homeassistant" / "mqtt.yaml"
AUTOMATIONS = ROOT / "src" / "homeassistant" / "automations.yaml"
UGV_CONTROL = ROOT / "src" / "drones" / "ugv" / "app" / "ugv_control.py"
UAV_BRIDGE = ROOT / "src" / "drones" / "uav" / "mavlink_bridge.py"


def test_homeassistant_mqtt_entities_for_drone_battery_and_status_exist():
    content = MQTT_YAML.read_text(encoding="utf-8")

    assert 'name: "UGV Battery"' in content
    assert 'name: "UGV Status"' in content
    assert 'name: "UAV Battery"' in content
    assert 'name: "UAV Status"' in content


def test_homeassistant_has_drone_control_buttons():
    content = MQTT_YAML.read_text(encoding="utf-8")

    assert 'name: "UGV Start Patrol"' in content
    assert 'name: "UGV Return Home"' in content
    assert 'name: "UGV Emergency Stop"' in content
    assert 'name: "UAV Inspect Zone"' in content
    assert 'name: "UAV Return Home"' in content
    assert 'name: "UAV STOP"' in content


def test_alarm_trigger_automations_dispatch_uav_and_ugv():
    content = AUTOMATIONS.read_text(encoding="utf-8")

    assert "id: alarm_triggered_dispatch_uav" in content
    assert 'topic: uav/command' in content
    assert '"cmd":"inspect_zone"' in content
    assert "id: alarm_triggered_dispatch_ugv" in content
    assert 'topic: ugv/command' in content
    assert '"cmd":"patrol"' in content


def test_intrusion_notification_automation_exists():
    content = AUTOMATIONS.read_text(encoding="utf-8")

    assert "id: drone_intrusion_notification" in content
    assert "topic: ugv/vision/detections" in content
    assert "topic: uav/vision/detections" in content
    assert "Intruso detectado por drone" in content


def test_unsigned_homeassistant_toggle_supported_in_ugv_and_uav():
    ugv_content = UGV_CONTROL.read_text(encoding="utf-8")
    uav_content = UAV_BRIDGE.read_text(encoding="utf-8")

    assert "ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_UGV" in ugv_content
    assert "unsigned_homeassistant_allowed" in ugv_content
    assert "ALLOW_UNSIGNED_HOMEASSISTANT_COMMANDS_UAV" in uav_content
    assert "unsigned_homeassistant_allowed" in uav_content
