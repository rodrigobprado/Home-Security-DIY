from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs" / "MATTER_THREAD_SEMESTER_REVIEW_RUNBOOK.md"
TEMPLATE = ROOT / "tasks" / "templates" / "matter_thread_review_template.md"


def test_matter_thread_semester_review_runbook_exists():
    content = RUNBOOK.read_text(encoding="utf-8")

    assert "Checklist da revisao" in content
    assert "adotar" in content
    assert "postergar" in content
    assert "matter_thread_review_template.md" in content


def test_matter_thread_review_template_exists():
    content = TEMPLATE.read_text(encoding="utf-8")

    assert "Template de Revisao Semestral Matter/Thread" in content
    assert "adotar/postergar" in content
