from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "DRONES_MOCK_TO_HARDWARE_RUNBOOK.md"


def test_runbook_covers_shadow_mode_and_golive_criteria():
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "Shadow mode" in content
    assert "Critérios de go-live" in content
    assert "0 comandos não assinados aceitos em produção" in content


def test_runbook_covers_rollback_and_required_evidence():
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "## Rollback" in content
    assert "## Evidência obrigatória" in content
