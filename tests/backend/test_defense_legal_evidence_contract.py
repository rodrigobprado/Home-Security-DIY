from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "DEFENSE_LEGAL_EVIDENCE_RUNBOOK.md"
TEMPLATE = ROOT / "tasks" / "templates" / "defense_legal_evidence_template.md"


def test_defense_legal_runbook_exists():
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "SP/RJ/MG" in content
    assert "2FA" in content
    assert "zonas de exclusao" in content
    assert "defense_legal_evidence_template.md" in content


def test_defense_legal_template_exists():
    content = TEMPLATE.read_text(encoding="utf-8")

    assert "Template de Evidencia Juridica e Tecnica" in content
    assert "PASS/FAIL" in content
