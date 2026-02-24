from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "src" / "docker-compose.yml"


def test_compose_defines_ugv_and_uav_services_in_drones_profile():
    content = COMPOSE.read_text(encoding="utf-8")

    assert "ugv:" in content
    assert "uav:" in content
    assert content.count('profiles: ["drones"]') >= 2
