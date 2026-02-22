from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UGV_CONTROL = ROOT / "src" / "drones" / "ugv" / "app" / "ugv_control.py"
UAV_BRIDGE = ROOT / "src" / "drones" / "uav" / "mavlink_bridge.py"
ENV_EXAMPLE = ROOT / "src" / ".env.example"


def test_unsigned_command_bypass_is_forbidden_outside_dev_test():
    ugv = UGV_CONTROL.read_text(encoding="utf-8")
    uav = UAV_BRIDGE.read_text(encoding="utf-8")

    assert "APP_ENV" in ugv
    assert "forbidden outside dev/test environments" in ugv
    assert "APP_ENV" in uav
    assert "forbidden outside dev/test environments" in uav


def test_env_example_declares_app_env_for_command_security():
    content = ENV_EXAMPLE.read_text(encoding="utf-8")

    assert "APP_ENV=production" in content
