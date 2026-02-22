from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UAV_BRIDGE = ROOT / "src" / "drones" / "uav" / "mavlink_bridge.py"
ENV_EXAMPLE = ROOT / "src" / ".env.example"
COMPLIANCE_DOC = ROOT / "docs" / "DRONE_REGULATORY_COMPLIANCE_BR.md"


def test_uav_bridge_has_altitude_geofence_and_rth_guards():
    content = UAV_BRIDGE.read_text(encoding="utf-8")

    assert "MAX_ALTITUDE_M_AGL_UAV" in content
    assert "RTH_BATTERY_THRESHOLD_UAV" in content
    assert "GEOFENCE_MIN_LAT_UAV" in content
    assert "GEOFENCE_MAX_LON_UAV" in content
    assert "enforce_regulatory_safety" in content
    assert "regulatory_reason" in content
    assert "uav_state[\"mode\"] = \"RTL\"" in content


def test_env_example_exposes_regulatory_uav_controls():
    content = ENV_EXAMPLE.read_text(encoding="utf-8")

    assert "MAX_ALTITUDE_M_AGL_UAV=120" in content
    assert "RTH_BATTERY_THRESHOLD_UAV=20" in content
    assert "UAV_MIN_SAFE_DISTANCE_M=30" in content
    assert "GEOFENCE_MIN_LAT_UAV" in content
    assert "GEOFENCE_MAX_LON_UAV" in content


def test_regulatory_checklist_document_exists():
    content = COMPLIANCE_DOC.read_text(encoding="utf-8")

    assert "ANAC" in content
    assert "SISANT" in content
    assert "DECEA" in content
    assert "ANATEL" in content
    assert "VLOS" in content
