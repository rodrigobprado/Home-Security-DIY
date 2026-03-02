from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGETS = [
    ROOT / "src" / "dashboard" / "backend" / "app" / "services" / "ha_client.py",
    ROOT / "src" / "dashboard" / "backend" / "app" / "services" / "frigate_client.py",
    ROOT / "src" / "dashboard" / "backend" / "app" / "routers" / "services.py",
    ROOT / "src" / "dashboard" / "backend" / "app" / "routers" / "ws.py",
]


def test_critical_integrations_do_not_swallow_generic_exceptions():
    for path in TARGETS:
        content = path.read_text(encoding="utf-8")
        assert "except Exception" not in content, f"Generic exception handler found in {path.name}"
        assert "\n        pass\n" not in content, f"Silent pass found in {path.name}"
