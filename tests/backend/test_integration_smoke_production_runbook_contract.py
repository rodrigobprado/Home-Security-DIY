from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "INTEGRATION_SMOKE_PRODUCTION_RUNBOOK.md"
TEMPLATE = ROOT / "tasks" / "templates" / "integration_smoke_execution_template.md"


def test_integration_smoke_production_runbook_exists():
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "scripts/integration_smoke_check.sh" in content
    assert "Criterio de aprovacao" in content
    assert "integration_smoke_execution_template.md" in content


def test_integration_smoke_execution_template_exists():
    content = TEMPLATE.read_text(encoding="utf-8")

    assert "Template de Execucao - Integration Smoke" in content
    assert "PASS/FAIL" in content
