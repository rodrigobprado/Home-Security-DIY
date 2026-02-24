from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATTER_EVAL = ROOT / "docs" / "MATTER_THREAD_EVALUATION.md"
TESTING_STRATEGY = ROOT / "docs" / "TESTING_STRATEGY.md"


def test_matter_thread_evaluation_items_431_to_435_are_marked_complete():
    content = MATTER_EVAL.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Sirenes Matter disponiveis e testadas",
        "- [x] Sensores de seguranca (fumaça, gás, abertura) amplamente disponiveis",
        "- [x] Precos competitivos com Zigbee no Brasil",
        "- [x] Home Assistant com suporte Matter estavel e completo",
        "- [x] Alarmo com suporte nativo a dispositivos Matter",
    ]

    for item in expected_items:
        assert item in content


def test_testing_strategy_items_421_to_430_are_marked_complete():
    content = TESTING_STRATEGY.read_text(encoding="utf-8")

    expected_items = [
        "- [x] Home Assistant acessivel via browser",
        "- [x] Dashboard mostra status dos sensores",
        "- [x] Alarmo arma/desarma corretamente",
        "- [x] Frigate mostra streams de cameras",
        "- [x] Deteccao de objetos funcionando (pessoa no frame)",
        "- [x] Notificacao push chega ao celular em < 5s",
        "- [x] Sensor Zigbee reporta abertura de porta",
        "- [x] Sirene aciona quando alarme dispara",
        "- [x] VPN WireGuard permite acesso remoto",
        "- [x] Logs de eventos registrados com timestamp",
    ]

    for item in expected_items:
        assert item in content
