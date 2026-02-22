from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "PHYSICAL_HARDENING_OPERATIONS_RUNBOOK.md"
TEMPLATE = ROOT / "tasks" / "templates" / "physical_hardening_field_audit_template.md"


def test_physical_hardening_operations_runbook_exists():
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "Cadencia recomendada" in content
    assert "Critérios de aprovação" in content or "Critérios de aprovacao" in content
    assert "physical_hardening_field_audit_template.md" in content


def test_physical_hardening_field_template_exists():
    content = TEMPLATE.read_text(encoding="utf-8")

    assert "Template de Auditoria de Campo - Hardening Fisico" in content
    assert "PASS/FAIL" in content
