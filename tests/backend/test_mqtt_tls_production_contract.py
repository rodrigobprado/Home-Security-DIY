from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROD_CONF = ROOT / "src" / "mosquitto" / "config" / "mosquitto.prod.conf"
AUDIT_SCRIPT = ROOT / "scripts" / "network_security_audit.sh"
CHECKLIST = ROOT / "docs" / "NETWORK_SECURITY_VLAN_CREDENTIALS_CHECKLIST.md"


def test_mosquitto_production_profile_is_tls_only():
    content = PROD_CONF.read_text(encoding="utf-8")

    assert "listener 8883" in content
    assert "cafile /mosquitto/certs/ca.crt" in content
    assert "certfile /mosquitto/certs/server.crt" in content
    assert "keyfile /mosquitto/certs/server.key" in content
    assert "listener 1883" not in content


def test_network_audit_checks_production_tls_baseline():
    content = AUDIT_SCRIPT.read_text(encoding="utf-8")

    assert "mosquitto.prod.conf" in content
    assert 'if [ "${APP_ENV:-}" = "production" ]; then' in content
    assert "listener 8883" in content


def test_network_checklist_mentions_tls_only_profile():
    content = CHECKLIST.read_text(encoding="utf-8")

    assert "Perfil de produção TLS-only versionado" in content
