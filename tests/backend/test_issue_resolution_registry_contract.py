import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "tasks" / "issue_resolution_registry.json"

PENDING_CHECKBOX = re.compile(r"^\s*[-*]\s*\[ \]", re.MULTILINE)
DEFAULT_PENDING_TERMS = [
    r"\bpendente\b",
    r"\bpendências\b",
    r"\bplanejad[oa]s?\b",
    r"\bprevist[oa]s?\b",
    r"\bTODO\b",
    r"\bbacklog\b",
]


def test_issue_resolution_registry_schema_and_files_exist():
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    issues = payload.get("issues", [])

    assert isinstance(issues, list)
    assert issues, "Registry must contain at least one resolved issue"

    for item in issues:
        assert {"issue", "priority", "target", "type", "resolved_on"}.issubset(item)
        assert (ROOT / item["target"]).exists(), f"Target file missing: {item['target']}"


def test_registry_targets_have_no_unchecked_checkboxes_when_type_is_checklist():
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))

    for item in payload.get("issues", []):
        if item["type"] != "checklist":
            continue
        content = (ROOT / item["target"]).read_text(encoding="utf-8")
        assert not PENDING_CHECKBOX.search(content), (
            f"Unchecked checklist found in {item['target']} for issue #{item['issue']}"
        )


def test_registry_targets_have_no_pending_terms_when_type_is_textual():
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))

    for item in payload.get("issues", []):
        if item["type"] != "textual":
            continue
        content = (ROOT / item["target"]).read_text(encoding="utf-8")
        forbidden_patterns = item.get("forbidden_patterns") or DEFAULT_PENDING_TERMS
        for pattern in forbidden_patterns:
            assert not re.search(pattern, content, re.IGNORECASE | re.MULTILINE), (
                f"Forbidden textual marker {pattern!r} still present in {item['target']} for issue #{item['issue']}"
            )
