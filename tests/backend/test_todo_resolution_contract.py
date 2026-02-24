from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_todo_resolution_markers_for_issues_402_to_380():
    repositories = _read(ROOT / "repositories" / "REPOSITORIES_STRUCTURE.md")
    rules_general = _read(ROOT / "rules" / "RULES_GENERAL.md")
    rules_technical = _read(ROOT / "rules" / "RULES_TECHNICAL.md")
    tasks_status = _read(ROOT / "tasks" / "TASKS_STATUS_OVERVIEW.md")
    workflows = _read(ROOT / "agents" / "AGENTS_WORKFLOWS.md")
    agents_overview = _read(ROOT / "agents" / "AGENTS_OVERVIEW.md")
    agents_config = _read(ROOT / "agents" / "AGENTS_CONFIG.md")
    project_overview = _read(ROOT / "PROJECT_OVERVIEW.md")
    standards = _read(ROOT / "standards" / "STANDARDS_TO_RESEARCH.md")
    docs_structure = _read(ROOT / "docs" / "DOCS_STRUCTURE.md")

    assert "Pendência resolvida: estratégia de repositório definida" in repositories
    assert "seções pendentes" in rules_general
    assert "Pendências de seleção tecnológica resolvidas" in rules_technical
    assert "Pendência de documentação de diagramas resolvida" in rules_technical
    assert "Pendência resolvida: fluxo operacional de status está definido e em uso." in tasks_status
    assert "Pendência resolvida: workflow atualizado para modelo GitHub Issues + PR + CI." in workflows
    assert "Pendência resolvida: ordem de execução da Fase 2 documentada" in agents_overview
    assert "Pendência resolvida: diretórios de memória e permissões operacionais definidos." in agents_config
    assert "Pendência resolvida: definição de cenários-base e estratégia de derivação registrada." in project_overview
    assert "Pendência resolvida: risco cibernético mapeado com mitigação" in project_overview
    assert "- [x] Escopo da ISO/IEC 27001 aplicado ao contexto IoT residencial documentado." in standards
    assert "Pendência resolvida: estrutura documental atualizada" in docs_structure
