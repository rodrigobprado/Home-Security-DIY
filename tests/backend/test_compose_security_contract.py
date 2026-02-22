from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "src" / "docker-compose.yml"


def test_dashboard_api_is_loopback_only_in_compose():
    content = COMPOSE.read_text(encoding="utf-8")

    assert '"127.0.0.1:8000:8000"' in content
    assert '"8000:8000"' not in content


def test_mqtt_tls_listener_is_exposed_in_loopback():
    content = COMPOSE.read_text(encoding="utf-8")

    assert '"127.0.0.1:8883:8883"' in content


def test_compose_has_healthchecks_for_critical_services():
    content = COMPOSE.read_text(encoding="utf-8")

    for service_name in (
        "postgres:",
        "mosquitto:",
        "zigbee2mqtt:",
        "frigate:",
        "homeassistant:",
        "dashboard-api:",
        "dashboard-frontend:",
    ):
        assert service_name in content

    # Contract-level check: critical services now define healthcheck in compose.
    assert content.count("healthcheck:") >= 7
