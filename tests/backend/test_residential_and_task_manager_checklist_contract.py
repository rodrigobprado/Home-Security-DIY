from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI_SCENARIOS = ROOT / "wiki" / "Cenarios-Residenciais.md"
TASK_MANAGER_MEMORY = ROOT / "agents" / "Agente_Gestor_Tarefas" / "MEMORY_LOCAL.md"


def test_residential_scenarios_checklist_items_504_to_518_are_marked_complete():
    content = WIKI_SCENARIOS.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Perímetro fechado e em bom estado",
        "- [x] Iluminação externa funcionando (constante ou sensor)",
        "- [x] Portões com fechadura de segurança",
        "- [x] Portas reforçadas com fechadura multiponto",
        "- [x] Janelas térreo com grades ou vidro laminado",
        "- [x] Batentes fixados com parafusos longos",
        "- [x] Paisagismo não cria esconderijos",
        "- [x] Objetos de valor não visíveis de fora",
        "- [x] Câmeras posicionadas conforme diagrama do cenário",
        "- [x] Sensores de abertura em todos os pontos de entrada",
        "- [x] Sensores PIR cobrindo áreas críticas",
        "- [x] Sirene interna e externa instaladas",
        "- [x] Nobreak dimensionado (ver [Resiliência](Resiliencia))",
        "- [x] 4G como canal de notificação de backup",
        "- [x] Contatos de emergência cadastrados no Home Assistant",
    ]

    for item in expected_items:
        assert item in content


def test_task_manager_memory_item_503_is_marked_complete():
    content = TASK_MANAGER_MEMORY.read_text(encoding="utf-8")

    assert "- [x] Estabelecer cadência de revisão do backlog (semanal? quinzenal?)" in content
