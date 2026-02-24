from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "rules" / "RULES_COMPLIANCE_AND_STANDARDS.md"


def test_rules_checklist_items_589_to_602_are_marked_complete():
    content = RULES.read_text(encoding="utf-8")

    required_done_items = [
        "- [x] Configurar zonas de exclusão de disparo (entradas de serviço, calçada)",
        "- [x] Testar failover de comunicação (Wi-Fi → LoRa)",
        "- [x] Documentar inventário de dispositivos",
        "- [x] Configurar rotação automática de gravações",
        "- [x] Configurar alertas de falha de energia",
        "- [x] Testar acesso via VPN",
        "- [x] Verificar logs de acesso",
        "- [x] Configurar alertas de bateria baixa em fechaduras eletrônicas",
        "- [x] Testar iluminação noturna com câmeras",
        "- [x] Documentar rotas de patrulha programadas",
        "- [x] Testar navegação autônoma em modo seguro",
        "- [x] Verificar logs de operação (imutabilidade)",
        "- [x] Testar integração com Home Assistant",
        "- [x] Calibrar detecção de IA (evitar falsos positivos)",
    ]

    for item in required_done_items:
        assert item in content
