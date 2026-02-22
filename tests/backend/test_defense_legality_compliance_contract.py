from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEGAL_DOC = ROOT / "docs" / "LEGALIDADE_MODULO_DEFESA_SP_RJ_MG.md"
DEFENSE_CONTROLLER = ROOT / "src" / "drones" / "common" / "defense_controller.py"


def test_state_level_legal_checklist_document_exists():
    content = LEGAL_DOC.read_text(encoding="utf-8")

    assert "São Paulo (SP)" in content
    assert "Rio de Janeiro (RJ)" in content
    assert "Minas Gerais (MG)" in content
    assert "Parecer jurídico" in content


def test_legal_doc_references_technical_safety_guards():
    content = LEGAL_DOC.read_text(encoding="utf-8")
    controller = DEFENSE_CONTROLLER.read_text(encoding="utf-8")

    assert "modo automático" in content.lower()
    assert "PIN + TOTP" in content
    assert "trilha de auditoria imutável" in content
    assert "automatic_mode_forbidden" in controller
