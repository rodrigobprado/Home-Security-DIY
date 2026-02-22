from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVALUATION = ROOT / "docs" / "MATTER_THREAD_EVALUATION.md"
DECISION = ROOT / "docs" / "MATTER_THREAD_DECISION_2026-02-22.md"


def test_matter_evaluation_contains_operational_decision_and_review_date():
    content = EVALUATION.read_text(encoding="utf-8")

    assert "Decisao operacional registrada em 2026-02-22" in content
    assert "docs/MATTER_THREAD_DECISION_2026-02-22.md" in content
    assert "Proxima revisao" in content
    assert "2026-08-22" in content


def test_matter_decision_log_contains_migration_checklist():
    content = DECISION.read_text(encoding="utf-8")

    assert "Checklist objetivo de migração" in content
    assert "Sirenes Matter disponíveis" in content
    assert "não migrar agora" in content
    assert "2026-08-22" in content
