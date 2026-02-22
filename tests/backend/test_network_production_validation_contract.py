from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAYBOOK = ROOT / "docs" / "NETWORK_PRODUCTION_VALIDATION_PLAYBOOK.md"
TEMPLATE = ROOT / "tasks" / "templates" / "network_production_validation_template.md"


def test_network_production_playbook_exists():
    content = PLAYBOOK.read_text(encoding="utf-8")

    assert "VLAN 20" in content
    assert "VLAN 30" in content
    assert "MQTT" in content
    assert "network_production_validation_template.md" in content


def test_network_production_template_exists():
    content = TEMPLATE.read_text(encoding="utf-8")

    assert "Template de Validacao de Rede em Producao" in content
    assert "PASS/FAIL" in content
