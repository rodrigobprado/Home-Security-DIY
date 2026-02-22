from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKLIST = ROOT / "docs" / "NETWORK_SECURITY_VLAN_CREDENTIALS_CHECKLIST.md"
AUDIT_SCRIPT = ROOT / "scripts" / "network_security_audit.sh"
MOSQUITTO_CONF = ROOT / "src" / "mosquitto" / "config" / "mosquitto.conf"
Z2M_CONF = ROOT / "src" / "zigbee2mqtt" / "configuration.yaml"


def test_network_compliance_checklist_exists():
    content = CHECKLIST.read_text(encoding="utf-8")

    assert "Segmentação de rede (VLANs)" in content
    assert "MQTT/TLS" in content
    assert "Gestão de credenciais" in content
    assert "scripts/network_security_audit.sh" in content


def test_network_audit_script_checks_core_controls():
    content = AUDIT_SCRIPT.read_text(encoding="utf-8")

    assert "allow_anonymous false" in content
    assert "acl_file" in content
    assert "permit_join" in content
    assert "VLAN30 → Internet: DENY ALL" in content


def test_core_repo_network_security_baselines_present():
    mosq = MOSQUITTO_CONF.read_text(encoding="utf-8")
    z2m = Z2M_CONF.read_text(encoding="utf-8")

    assert "allow_anonymous false" in mosq
    assert "acl_file" in mosq
    assert "permit_join: false" in z2m
