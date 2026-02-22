from pathlib import Path


GUIDE = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "GUIA_MONTAGEM_UGV.md"
)


def test_ugv_guide_has_current_pinout_and_no_gpio_18_19_usage():
    content = GUIDE.read_text(encoding="utf-8")

    assert "RPWM_R | 25" in content
    assert "LPWM_R | 26" in content
    assert "GPIO 18/19" in content
    assert "devem permanecer **sem uso**" in content


def test_ugv_guide_has_pre_power_and_post_validation_checklists():
    content = GUIDE.read_text(encoding="utf-8")

    assert "Checklist pre-energizacao" in content
    assert "Checklist de validacao pos-montagem" in content
    assert "Telemetria serial recebida" in content
    assert "ugv/status" in content
