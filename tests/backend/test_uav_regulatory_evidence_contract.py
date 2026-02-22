from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "UAV_REGULATORY_EVIDENCE_RUNBOOK.md"
TEMPLATE = ROOT / "tasks" / "templates" / "uav_regulatory_evidence_template.md"


def test_uav_regulatory_runbook_exists():
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "ANAC/SISANT/DECEA/ANATEL" in content
    assert "Checklist operacional" in content
    assert "Evidencia minima" in content
    assert "uav_regulatory_evidence_template.md" in content


def test_uav_regulatory_template_exists():
    content = TEMPLATE.read_text(encoding="utf-8")

    assert "Template de Evidencia Regulatoria UAV" in content
    assert "PASS/FAIL" in content
