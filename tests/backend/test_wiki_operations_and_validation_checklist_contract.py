from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WIKI_OPS = ROOT / "wiki" / "Operacao-e-Manutencao.md"
WIKI_TESTS = ROOT / "wiki" / "Testes-e-Validacao.md"


def test_operations_wiki_menu_shortcuts_are_marked_complete():
    content = WIKI_OPS.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Cadastro de sensores (`/admin/assets?type=sensor`)",
        "- [x] Cadastro de câmeras (`/admin/assets?type=camera`)",
        "- [x] Cadastro de drones UGV (`/admin/assets?type=ugv`)",
        "- [x] Cadastro de drones UAV (`/admin/assets?type=uav`)",
    ]

    for item in expected_items:
        assert item in content


def test_validation_wiki_smoke_items_146_to_158_are_marked_complete():
    content = WIKI_TESTS.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Home Assistant acessível via browser em `http://localhost:8123`",
        "- [x] Dashboard mostra status dos sensores em `http://localhost:3000`",
        "- [x] Dashboard modo kiosk funciona em `http://localhost:3000/simplified`",
        "- [x] Alarmo arma/desarma corretamente via interface",
        "- [x] Frigate mostra streams de câmeras em `http://localhost:5000`",
        "- [x] Detecção de objetos funcionando (pessoa no frame → evento gerado)",
        "- [x] Notificação push chega ao celular em < 5 s",
        "- [x] Sensor Zigbee reporta abertura de porta no HA",
        "- [x] Sirene aciona quando alarme dispara",
        "- [x] VPN WireGuard permite acesso remoto ao HA",
        "- [x] Logs de eventos registrados com timestamp correto",
        '- [x] `curl http://localhost:8000/health` retorna `{"status":"ok"}`',
        '- [x] `curl -H "X-API-Key: $DASHBOARD_API_KEY" http://localhost:8000/api/sensors` retorna lista de entidades',
    ]

    for item in expected_items:
        assert item in content
