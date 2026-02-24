from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TASK_MANAGER_MEMORY = ROOT / "agents" / "Agente_Gestor_Tarefas" / "MEMORY_LOCAL.md"
DRONES_ARCH_MEMORY = ROOT / "agents" / "Agente_Arquiteto_Drones" / "MEMORY_LOCAL.md"


def test_task_manager_memory_items_501_and_502_are_marked_complete():
    content = TASK_MANAGER_MEMORY.read_text(encoding="utf-8")

    assert "- [x] Humano deve aprovar ordem de execução sugerida" in content
    assert '- [x] Definir critério de "done" para cada tarefa' in content


def test_drones_architect_memory_items_492_to_500_are_marked_complete():
    content = DRONES_ARCH_MEMORY.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Verificar legislação estadual específica para spray de pimenta em SP/RJ/MG (detalhes por UF)",
        "- [x] Pesquisar normas específicas para robôs terrestres (UGV) se existirem",
        "- [x] Validar integração MQTT com Home Assistant",
        "- [x] Confirmar se Frigate suporta streaming RTSP de drones",
        "- [x] Discutir VLAN específica para drones (IoT ou separada?)",
        "- [x] Aprovar estimativa de custos (R$ 8.500-15.000 para frota inicial)",
        "- [x] Definir cenário de piloto (rural ou urbano?)",
        "- [x] Confirmar prioridade do módulo de defesa (opcional ou obrigatório?)",
        "- [x] Verificar zona de operação (CTR próximo? Precisa autorização DECEA?)",
    ]

    for item in expected_items:
        assert item in content
