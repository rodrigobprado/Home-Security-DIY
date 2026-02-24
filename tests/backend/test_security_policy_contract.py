from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SECURITY_POLICY = ROOT / "SECURITY.md"


def test_security_policy_includes_private_reporting_channel():
    content = SECURITY_POLICY.read_text(encoding="utf-8")

    assert "NÃO abra uma issue pública" in content
    assert "/security/advisories/new" in content


def test_security_policy_defines_sla_by_severity():
    content = SECURITY_POLICY.read_text(encoding="utf-8")

    assert "SLA de resposta por severidade" in content
    assert "Crítica" in content
    assert "Alta" in content
    assert "Média" in content
    assert "Baixa" in content
