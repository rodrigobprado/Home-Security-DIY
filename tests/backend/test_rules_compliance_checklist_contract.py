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


def test_rules_checklist_items_562_to_588_are_marked_complete():
    content = RULES.read_text(encoding="utf-8")

    required_done_items = [
        "- [x] Verificar legislação municipal sobre cercas elétricas",
        "- [x] Documentar ângulos de câmera (área privada vs. pública)",
        "- [x] Definir política de retenção de gravações",
        "- [x] Avaliar necessidade de SPDA",
        "- [x] Selecionar fechaduras com grau de segurança adequado (NBR 14913)",
        "- [x] Planejar iluminação com níveis adequados (mín. 50 lux em entradas)",
        "- [x] Verificar peso do drone (>250g requer registro ANAC)",
        "- [x] Registrar drone no SISANT/DECEA",
        "- [x] Verificar zonas de voo permitidas (AIS DECEA)",
        "- [x] Homologar módulos de rádio (Wi-Fi, LoRa) junto à ANATEL",
        "- [x] Verificar legislação estadual sobre spray de pimenta",
        "- [x] Confirmar que modo automático de disparo está DESABILITADO (REGRA-DRONE-17/23)",
        "- [x] Consultar advogado sobre responsabilidade civil e criminal do módulo de defesa (REGRA-DRONE-25)",
        "- [x] Instalar DPS no quadro de distribuição",
        "- [x] Configurar VLANs para IoT e câmeras",
        "- [x] Alterar TODAS as senhas padrão",
        "- [x] Desabilitar serviços desnecessários em cada dispositivo",
        "- [x] Instalar placas de aviso de monitoramento",
        "- [x] Instalar protetor de cilindro em portas de entrada",
        "- [x] Verificar uniformidade de iluminação (sem pontos escuros)",
        "- [x] Confirmar que iluminação não causa ofuscamento em câmeras",
        "- [x] Configurar geofence com área de operação autorizada",
        "- [x] Configurar RTH (Return To Home) automático",
        "- [x] Configurar limites de bateria para retorno (20%)",
        "- [x] Configurar autenticação 2FA para módulo de defesa",
        "- [x] Verificar que detecção de crianças e animais está ativa e bloqueando disparo (REGRA-DRONE-24)",
        "- [x] Confirmar que modo semi-automático é o máximo configurado (REGRA-DRONE-23)",
    ]

    for item in required_done_items:
        assert item in content
