from pathlib import Path


UGV_CONTROL = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "ugv"
    / "app"
    / "ugv_control.py"
)


def test_patrol_command_reports_not_implemented_status():
    content = UGV_CONTROL.read_text(encoding="utf-8")

    assert "elif command == 'patrol':" in content
    assert "\"status\": \"not_implemented\"" in content
    assert "\"command\": \"patrol\"" in content
    assert "MQTT_TOPIC_STATUS" in content
