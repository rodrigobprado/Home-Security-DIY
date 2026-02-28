from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UGV_CONTROL = ROOT / "src" / "drones" / "ugv" / "app" / "ugv_control.py"
UAV_BRIDGE = ROOT / "src" / "drones" / "uav" / "mavlink_bridge.py"
UAV_VISION = ROOT / "src" / "drones" / "uav" / "uav_vision.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ugv_and_uav_use_logging_instead_of_print_runtime():
    ugv = _read(UGV_CONTROL)
    uav = _read(UAV_BRIDGE)
    vision = _read(UAV_VISION)

    assert "print(" not in ugv
    assert "print(" not in uav
    assert "print(" not in vision

    assert "logger =" in ugv
    assert "logger =" in uav
    assert "logger =" in vision


def test_mock_fallback_requires_explicit_dev_test_toggle():
    ugv = _read(UGV_CONTROL)
    uav = _read(UAV_BRIDGE)

    assert "DRONES_ALLOW_MOCK_IMPORTS" in ugv
    assert "DRONES_ALLOW_MOCK_IMPORTS" in uav
    assert "refuses silent mock fallback in production" in ugv
    assert "refuses silent mock fallback in production" in uav
