from pathlib import Path


GUIDE = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "GUIA_MONTAGEM_UAV.md"
)


def test_uav_guide_references_mavlink_bridge_and_mqtt_topics():
    content = GUIDE.read_text(encoding="utf-8")

    assert "src/drones/uav/mavlink_bridge.py" in content
    assert "uav/status" in content
    assert "uav/location" in content
    assert "uav/command" in content
    assert "uav/lora/command" in content


def test_uav_guide_contains_vlos_and_regulatory_constraints():
    content = GUIDE.read_text(encoding="utf-8")

    assert "VLOS" in content
    assert "SISANT" in content
    assert "não recreativa" in content
