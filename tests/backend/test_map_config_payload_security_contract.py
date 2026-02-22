from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ALERTS_ROUTER = ROOT / "src" / "dashboard" / "backend" / "app" / "routers" / "alerts.py"


def test_map_config_payload_has_size_and_format_validation():
    content = ALERTS_ROUTER.read_text(encoding="utf-8")

    assert "MAX_FLOORPLAN_DATA_URL_LENGTH" in content
    assert "floorplan image payload exceeds maximum allowed size" in content
    assert "data:image/" in content
    assert ";base64," in content
