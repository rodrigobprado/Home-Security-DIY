import httpx
import pytest
from fastapi import Depends, FastAPI

from app.db.session import get_db
from app.routers import alerts, cameras, sensors, services, ws
from app.security import require_api_key


class _FakeScalars:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows


class _FakeResult:
    def __init__(self, rows):
        self._rows = rows

    def scalars(self):
        return _FakeScalars(self._rows)


class _FakeAlert:
    def __init__(self):
        from datetime import datetime, timezone

        self.id = 1
        self.timestamp = datetime.now(timezone.utc)
        self.entity_id = "alarm_control_panel.alarmo"
        self.event_type = "state_changed"
        self.old_state = "disarmed"
        self.new_state = "armed_home"
        self.severity = "warning"
        self.message = "mock alert"


class _FakeSession:
    async def execute(self, _stmt):
        return _FakeResult([_FakeAlert()])

    def add(self, _entry):
        return None

    async def commit(self):
        return None


async def _override_get_db():
    yield _FakeSession()


def _build_test_app():
    app = FastAPI()
    app.include_router(ws.router)
    app.include_router(sensors.router, dependencies=[Depends(require_api_key)])
    app.include_router(cameras.router, dependencies=[Depends(require_api_key)])
    app.include_router(alerts.router, dependencies=[Depends(require_api_key)])
    app.include_router(services.router, dependencies=[Depends(require_api_key)])
    app.dependency_overrides[get_db] = _override_get_db
    return app


@pytest.mark.anyio
async def test_http_routes_require_api_key():
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        assert (await client.get("/api/sensors")).status_code == 403
        assert (await client.get("/api/cameras/events")).status_code == 403
        assert (await client.get("/api/alerts")).status_code == 403
        assert (await client.get("/api/services/status")).status_code == 403


@pytest.mark.anyio
async def test_sensors_route_with_api_key(monkeypatch):
    from app.services import ha_client

    monkeypatch.setattr(ha_client, "get_all_states", lambda: {"binary_sensor.porta_entrada": {"state": "off"}})

    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/api/sensors", headers={"X-API-Key": "test-api-key"})
    assert resp.status_code == 200
    assert "states" in resp.json()


@pytest.mark.anyio
async def test_cameras_routes_with_api_key(monkeypatch):
    from app.services import frigate_client

    async def _snapshot(_camera):
        return b"fake-jpeg"

    async def _events(camera=None, label=None, limit=20):
        return [{"id": "evt-1", "camera": camera, "label": label, "limit": limit}]

    monkeypatch.setattr(frigate_client, "get_snapshot", _snapshot)
    monkeypatch.setattr(frigate_client, "get_events", _events)

    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        snap = await client.get("/api/cameras/cam_entrada/snapshot", headers={"X-API-Key": "test-api-key"})
        evts = await client.get("/api/cameras/events", headers={"X-API-Key": "test-api-key"})

    assert snap.status_code == 200
    assert snap.headers["content-type"] == "image/jpeg"
    assert evts.status_code == 200
    assert isinstance(evts.json(), list)


@pytest.mark.anyio
async def test_alerts_route_with_api_key():
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/api/alerts", headers={"X-API-Key": "test-api-key"})

    assert resp.status_code == 200
    payload = resp.json()
    assert isinstance(payload, list)
    assert payload[0]["entity_id"] == "alarm_control_panel.alarmo"


@pytest.mark.anyio
async def test_services_route_with_api_key(monkeypatch):
    from app.routers import services as services_router

    async def _ok(_url):
        return "online"

    monkeypatch.setattr(services_router, "_check_http", _ok)
    monkeypatch.setattr(services_router.ha_client, "get_all_states", lambda: {"alarm_control_panel.alarmo": {"state": "disarmed"}})

    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        resp = await client.get("/api/services/status", headers={"X-API-Key": "test-api-key"})
        metrics = await client.get("/api/services/ws-metrics", headers={"X-API-Key": "test-api-key"})

    assert resp.status_code == 200
    assert resp.json()["services"]["ha_websocket"] == "online"
    assert metrics.status_code == 200
    assert "ws_metrics" in metrics.json()
