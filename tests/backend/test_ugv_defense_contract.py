from pathlib import Path


UGV_CONTROL = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "ugv"
    / "app"
    / "ugv_control.py"
)

DEFENSE_CONTROLLER = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "drones"
    / "common"
    / "defense_controller.py"
)

DEFENSE_DOC = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "DRONE_DEFENSE_IMPLEMENTATION.md"
)


def test_ugv_control_supports_defense_safety_controls():
    content = UGV_CONTROL.read_text(encoding="utf-8")

    assert "MQTT_TOPIC_VISION_SAFETY" in content
    assert "MQTT_TOPIC_DEFENSE_AUDIT" in content
    assert "DEFENSE_TOTP_SECRET_UGV" in content
    assert "DEFENSE_EXCLUSION_ZONES_UGV" in content
    assert 'command == "defense_mode"' in content
    assert 'command == "defense_fire"' in content
    assert "automatic_mode_forbidden" in content


def test_defense_controller_enforces_totp_and_hash_audit():
    content = DEFENSE_CONTROLLER.read_text(encoding="utf-8")

    assert "_verify_totp" in content
    assert "_append_audit" in content
    assert "hashlib.sha256" in content
    assert "MODE_SEMI_AUTO" in content
    assert "automatic_mode_forbidden" in content
    assert "warning_seconds" in content


def test_defense_documentation_mentions_legal_review_and_actuator_spec():
    content = DEFENSE_DOC.read_text(encoding="utf-8")

    assert "Especificacao de atuador fisico" in content
    assert "Consulta juridica" in content
    assert "modo automatico" in content.lower()
