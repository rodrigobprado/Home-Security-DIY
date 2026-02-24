from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"


def test_root_readme_exists_and_has_core_operational_sections():
    content = README.read_text(encoding="utf-8")

    assert content.startswith("# Home Security DIY")
    assert "## Como começar" in content
    assert "## Estrutura do repositório" in content
    assert "## Contribuição" in content
    assert "## Licença e Aviso Legal" in content
