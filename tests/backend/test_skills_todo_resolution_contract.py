from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SKILLS_DOCS = ROOT / "skills" / "SKILLS_DOCS.md"
SKILL_TEMPLATES = ROOT / "skills" / "SKILL_TEMPLATES.md"
SKILLS_OVERVIEW = ROOT / "skills" / "SKILLS_OVERVIEW.md"


def test_skills_todo_resolution_markers_exist():
    docs_content = SKILLS_DOCS.read_text(encoding="utf-8")
    templates_content = SKILL_TEMPLATES.read_text(encoding="utf-8")
    overview_content = SKILLS_OVERVIEW.read_text(encoding="utf-8")

    assert "Pendência resolvida: catálogo inicial de skills de documentação consolidado." in docs_content
    assert "Pendência resolvida: template substituído por inventário real de skills de desenvolvimento." in templates_content
    assert "Pendência resolvida: visão geral atualizada com skills documentadas por domínio." in overview_content
