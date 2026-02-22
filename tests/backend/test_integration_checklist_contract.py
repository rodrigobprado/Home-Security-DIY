from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKLIST = ROOT / "docs" / "INTEGRATION_VALIDATION_CHECKLIST.md"
SCRIPT = ROOT / "scripts" / "integration_smoke_check.sh"


def test_integration_validation_checklist_exists():
    content = CHECKLIST.read_text(encoding="utf-8")

    assert "Infraestrutura base" in content
    assert "Câmeras e detecção" in content
    assert "Sensores e alarme" in content
    assert "Conectividade e backup" in content
    assert "scripts/integration_smoke_check.sh" in content


def test_integration_smoke_script_checks_core_endpoints():
    content = SCRIPT.read_text(encoding="utf-8")

    assert "http://localhost:8123" in content
    assert "http://localhost:3000" in content
    assert "http://localhost:8000/health" in content
    assert "http://localhost:5000" in content
    assert "DASHBOARD_API_KEY" in content
