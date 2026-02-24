from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HARDENING_DOC = ROOT / "docs" / "HARDENING_ANTI_TAMPER.md"


def test_hardening_anti_tamper_items_416_to_420_are_marked_complete():
    content = HARDENING_DOC.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Criptografia de disco (LUKS) ativa.",
        "- [x] Dropbear SSH configurado para unlock remoto.",
        "- [x] Senha de BIOS configurada e boot USB desativado.",
        "- [x] Servidor fisicamente seguro/oculto.",
        "- [x] Backup automático off-site configurado.",
    ]

    for item in expected_items:
        assert item in content
