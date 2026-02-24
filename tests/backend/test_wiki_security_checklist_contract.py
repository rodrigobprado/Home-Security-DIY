from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI_SECURITY = ROOT / "wiki" / "Seguranca-e-Compliance.md"


def test_wiki_security_segmentacao_checklist_is_marked_complete():
    content = WIKI_SECURITY.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Política de backup off-site agendada e validada",
        "- [x] VLAN 10 definida para gestão com acesso controlado",
        "- [x] VLAN 20 definida para IoT sem acesso à internet",
        "- [x] VLAN 30 definida para câmeras sem acesso à internet",
        "- [x] Regra `VLAN 30 -> WAN: DENY ALL` aplicada",
        "- [x] Regra `VLAN 20 -> WAN: DENY ALL` aplicada",
        "- [x] Acesso remoto restrito a VPN",
        "- [x] Port forwarding direto desabilitado",
    ]

    for item in expected_items:
        assert item in content


def test_wiki_security_hardening_checklists_are_marked_complete():
    content = WIKI_SECURITY.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Mínimo 16 caracteres para serviços críticos (HA, SSH, MQTT)",
        "- [x] Senha única por serviço (nunca reutilizar)",
        "- [x] Gerenciador de senhas em uso (Bitwarden, KeePass)",
        "- [x] Home Assistant: TOTP habilitado para todos os usuários",
        "- [x] `PasswordAuthentication no`",
        "- [x] `PermitRootLogin no`",
        "- [x] UPnP desabilitado no roteador",
        "- [x] Port forwarding: nenhum",
    ]

    for item in expected_items:
        assert item in content
