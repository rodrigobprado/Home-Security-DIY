from pathlib import Path


UGV_CONTROL = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "ugv"
    / "app"
    / "ugv_control.py"
)


def test_patrol_command_starts_route_and_no_longer_reports_not_implemented():
    content = UGV_CONTROL.read_text(encoding="utf-8")

    assert "elif command == 'patrol':" in content
    assert "\"started\"" in content
    assert "started_mqtt_only" in content
    assert "\"command\": \"patrol\"" in content
    assert "MQTT_TOPIC_STATUS" in content
    assert "MQTT_TOPIC_WAYPOINTS_SET" in content
