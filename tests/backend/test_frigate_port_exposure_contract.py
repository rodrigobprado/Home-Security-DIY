from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "src" / "docker-compose.yml"
CHECKLIST = ROOT / "docs" / "NETWORK_SECURITY_VLAN_CREDENTIALS_CHECKLIST.md"


def test_frigate_ports_are_loopback_only():
    content = COMPOSE.read_text(encoding="utf-8")

    assert "127.0.0.1:8554:8554" in content
    assert "127.0.0.1:8555:8555" in content
    assert "127.0.0.1:8555:8555/udp" in content
    assert "- \"8554:8554\"" not in content
    assert "- \"8555:8555\"" not in content


def test_network_checklist_mentions_frigate_loopback_binding():
    content = CHECKLIST.read_text(encoding="utf-8")

    assert "Frigate (8554/8555) restrito a loopback" in content
