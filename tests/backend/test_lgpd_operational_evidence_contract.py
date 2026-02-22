from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "LGPD_OPERATIONAL_EVIDENCE_RUNBOOK.md"
TEMPLATE = ROOT / "tasks" / "templates" / "lgpd_field_evidence_template.md"


def test_lgpd_operational_runbook_exists_with_required_sections():
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "Checklist de campo" in content
    assert "Evidencia minima por item" in content
    assert "Frequencia" in content
    assert "tasks/templates/lgpd_field_evidence_template.md" in content


def test_lgpd_field_template_exists():
    content = TEMPLATE.read_text(encoding="utf-8")

    assert "Template de Evidencia de Campo LGPD" in content
    assert "Cameras validadas" in content
    assert "PASS/FAIL" in content
