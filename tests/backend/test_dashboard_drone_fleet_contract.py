from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAP_COMPONENT = ROOT / "src" / "dashboard" / "frontend" / "src" / "components" / "OperationalMap.jsx"
DRONES_ROUTER = ROOT / "src" / "dashboard" / "backend" / "app" / "routers" / "drones.py"
ALERTS_ROUTER = ROOT / "src" / "dashboard" / "backend" / "app" / "routers" / "alerts.py"
MAIN_API = ROOT / "src" / "dashboard" / "backend" / "app" / "main.py"


def test_operational_map_has_upload_realtime_and_route_history():
    content = MAP_COMPONENT.read_text(encoding="utf-8")

    assert "Upload planta" in content
    assert "routeHistory" in content
    assert "HISTORY_WINDOW_MS" in content
    assert "uav/command" not in content  # commands should go through backend API
    assert "/api/drones/command" in content
    assert "Start Patrol" in content
    assert "Return" in content
    assert "STOP" in content


def test_backend_exposes_drone_command_router():
    content = DRONES_ROUTER.read_text(encoding="utf-8")

    assert 'prefix="/api/drones"' in content
    assert '@router.post("/command")' in content
    assert "mqtt/publish" in content
    assert '"cmd": "patrol"' in content
    assert '"cmd": "return_home"' in content
    assert '"cmd": "stop"' in content


def test_backend_map_config_endpoints_exist():
    content = ALERTS_ROUTER.read_text(encoding="utf-8")

    assert '@router.get("/map/config")' in content
    assert '@router.put("/map/config")' in content
    assert "map.floorplan_image_data_url" in content
    assert "map.geo_bounds_json" in content


def test_main_registers_drones_router_and_http_methods():
    content = MAIN_API.read_text(encoding="utf-8")

    assert "from app.routers import alerts, cameras, drones, sensors, services, ws" in content
    assert "app.include_router(drones.router" in content
    assert 'allow_methods=["GET", "POST", "PUT", "OPTIONS"]' in content
