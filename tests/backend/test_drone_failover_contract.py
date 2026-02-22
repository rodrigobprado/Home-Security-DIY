from pathlib import Path

UGV_CONTROL = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "ugv"
    / "app"
    / "ugv_control.py"
)

UAV_BRIDGE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "uav"
    / "mavlink_bridge.py"
)


def test_ugv_has_failover_topics_and_timeout_logic():
    content = UGV_CONTROL.read_text(encoding="utf-8")

    assert "MQTT_TOPIC_LORA_CMD" in content
    assert "MQTT_TOPIC_LINK_METRICS" in content
    assert "MQTT_TOPIC_LINK_STATE" in content
    assert "FAILOVER_TIMEOUT_SECONDS" in content
    assert "wifi_timeout_or_low_rssi" in content


def test_uav_has_failover_topics_and_emergency_commands():
    content = UAV_BRIDGE.read_text(encoding="utf-8")

    assert "MQTT_TOPIC_LORA_CMD" in content
    assert "MQTT_TOPIC_LINK_METRICS" in content
    assert "MQTT_TOPIC_LINK_STATE" in content
    assert "FAILOVER_TIMEOUT_SECONDS" in content
    assert "cmd == 'rth'" in content
    assert "cmd == 'stop'" in content
