from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
QUICK_START = ROOT / "src" / "docs" / "QUICK_START.md"
ARCH_TECNICA = ROOT / "docs" / "ARQUITETURA_TECNICA.md"
ARCH_FISICA = ROOT / "docs" / "ARQUITETURA_SEGURANCA_FISICA.md"


def test_quick_start_items_460_to_465_are_marked_complete():
    content = QUICK_START.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Configurar VLANs para isolar câmeras e IoT ([docs/ARQUITETURA_TECNICA.md](../../docs/ARQUITETURA_TECNICA.md))",
        "- [x] Configurar VPN WireGuard para acesso remoto",
        "- [x] Configurar notificações Telegram",
        "- [x] Ajustar zonas de detecção do Frigate",
        "- [x] Instalar e configurar nobreak com monitoramento",
        "- [x] Criar backup automático das configurações",
    ]

    for item in expected_items:
        assert item in content


def test_arquitetura_tecnica_items_451_to_459_are_marked_complete():
    content = ARCH_TECNICA.read_text(encoding="utf-8")

    expected_items = [
        "- [x] VLANs configuradas e isoladas",
        "- [x] Câmeras sem acesso à internet",
        "- [x] Sensores IoT Wi-Fi sem acesso à internet",
        "- [x] Firewall com regras restritivas",
        "- [x] VPN configurada para acesso remoto",
        "- [x] Senhas de todos os dispositivos alteradas",
        "- [x] Firmware de câmeras atualizado",
        "- [x] Wi-Fi com WPA3 (ou WPA2-AES mínimo)",
        "- [x] SSID da rede IoT oculto (opcional)",
    ]

    for item in expected_items:
        assert item in content


def test_arquitetura_seguranca_fisica_items_450_and_related_are_marked_complete():
    content = ARCH_FISICA.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Perímetro fechado e em bom estado",
        "- [x] Cerca elétrica instalada e sinalizada (se aplicável)",
        "- [x] Portões com fechadura de segurança",
        "- [x] Iluminação externa funcionando",
        "- [x] Portas reforçadas com fechadura multiponto",
        "- [x] Janelas térreo com grades ou vidro reforçado",
        "- [x] Batentes fixados com parafusos longos",
        "- [x] Paisagismo não cria esconderijos",
        "- [x] Objetos de valor não visíveis de fora",
        "- [x] Plano de resposta documentado e conhecido por moradores",
        "- [x] Contatos de emergência cadastrados no sistema",
        "- [x] Números de emergência salvos (190, vizinhos)",
        "- [x] Nobreak instalado e testado",
        "- [x] Backup de configurações realizado",
        "- [x] Teste periódico do sistema (mensal)",
    ]

    for item in expected_items:
        assert item in content
