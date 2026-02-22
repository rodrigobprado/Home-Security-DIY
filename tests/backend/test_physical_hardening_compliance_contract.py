from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKLIST = ROOT / "docs" / "SEGURANCA_FISICA_HARDENING_CHECKLIST.md"
AUDIT_SCRIPT = ROOT / "scripts" / "physical_hardening_audit.sh"


def test_physical_hardening_checklist_exists_with_required_sections():
    content = CHECKLIST.read_text(encoding="utf-8")

    assert "Perímetro e barreiras físicas" in content
    assert "Iluminação e visibilidade" in content
    assert "Hardening do servidor" in content
    assert "Conformidade elétrica (NBR 5410)" in content
    assert "scripts/physical_hardening_audit.sh" in content


def test_physical_hardening_audit_script_has_core_checks():
    content = AUDIT_SCRIPT.read_text(encoding="utf-8")

    assert "PHYSICAL_HARDENING_AUDIT_" in content
    assert "lsblk -o TYPE" in content
    assert "scripts/backup.sh" in content
    assert "HARDENING_ANTI_TAMPER.md" in content
