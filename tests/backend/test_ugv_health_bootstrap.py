from pathlib import Path


UGV_CONTROL = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "ugv"
    / "app"
    / "ugv_control.py"
)


def test_heartbeat_is_reset_immediately_after_mqtt_connect():
    content = UGV_CONTROL.read_text(encoding="utf-8")

    connect_marker = "client.connect(MQTT_BROKER, MQTT_PORT, 60)"
    heartbeat_marker = "health.update_heartbeat()"
    loop_start_marker = "client.loop_start()"

    assert connect_marker in content
    assert heartbeat_marker in content
    assert loop_start_marker in content

    connect_pos = content.index(connect_marker)
    heartbeat_pos = content.index(heartbeat_marker, connect_pos)
    loop_start_pos = content.index(loop_start_marker, connect_pos)

    assert connect_pos < heartbeat_pos < loop_start_pos
