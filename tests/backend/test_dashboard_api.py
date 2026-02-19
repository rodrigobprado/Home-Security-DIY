import json

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

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


def test_http_routes_require_api_key():
    app = _build_test_app()
    client = TestClient(app)

    assert client.get("/api/sensors").status_code == 403
    assert client.get("/api/cameras/events").status_code == 403
    assert client.get("/api/alerts").status_code == 403
    assert client.get("/api/services/status").status_code == 403


def test_sensors_route_with_api_key(monkeypatch):
    from app.services import ha_client

    monkeypatch.setattr(ha_client, "get_all_states", lambda: {"binary_sensor.porta_entrada": {"state": "off"}})

    app = _build_test_app()
    client = TestClient(app)
    resp = client.get("/api/sensors", headers={"X-API-Key": "test-api-key"})

    assert resp.status_code == 200
    assert "states" in resp.json()


def test_cameras_routes_with_api_key(monkeypatch):
    from app.services import frigate_client

    async def _snapshot(_camera):
        return b"fake-jpeg"

    async def _events(camera=None, label=None, limit=20):
        return [{"id": "evt-1", "camera": camera, "label": label, "limit": limit}]

    monkeypatch.setattr(frigate_client, "get_snapshot", _snapshot)
    monkeypatch.setattr(frigate_client, "get_events", _events)

    app = _build_test_app()
    client = TestClient(app)

    snap = client.get("/api/cameras/cam_entrada/snapshot", headers={"X-API-Key": "test-api-key"})
    evts = client.get("/api/cameras/events", headers={"X-API-Key": "test-api-key"})

    assert snap.status_code == 200
    assert snap.headers["content-type"] == "image/jpeg"
    assert evts.status_code == 200
    assert isinstance(evts.json(), list)


def test_alerts_route_with_api_key():
    app = _build_test_app()
    client = TestClient(app)

    resp = client.get("/api/alerts", headers={"X-API-Key": "test-api-key"})

    assert resp.status_code == 200
    payload = resp.json()
    assert isinstance(payload, list)
    assert payload[0]["entity_id"] == "alarm_control_panel.alarmo"


def test_services_route_with_api_key(monkeypatch):
    from app.routers import services as services_router

    async def _ok(_url):
        return "online"

    monkeypatch.setattr(services_router, "_check_http", _ok)
    monkeypatch.setattr(services_router.ha_client, "get_all_states", lambda: {"alarm_control_panel.alarmo": {"state": "disarmed"}})

    app = _build_test_app()
    client = TestClient(app)
    resp = client.get("/api/services/status", headers={"X-API-Key": "test-api-key"})

    assert resp.status_code == 200
    assert resp.json()["services"]["ha_websocket"] == "online"

    metrics = client.get("/api/services/ws-metrics", headers={"X-API-Key": "test-api-key"})
    assert metrics.status_code == 200
    assert "ws_metrics" in metrics.json()


def test_ws_requires_api_key():
    app = _build_test_app()
    client = TestClient(app)

    with pytest.raises(WebSocketDisconnect):
        with client.websocket_connect("/ws"):
            pass


def test_ws_with_api_key(monkeypatch):
    from app.services import ha_client

    subscribed = []

    def _subscribe(cb):
        subscribed.append(cb)

    def _unsubscribe(cb):
        if cb in subscribed:
            subscribed.remove(cb)

    monkeypatch.setattr(ha_client, "subscribe", _subscribe)
    monkeypatch.setattr(ha_client, "unsubscribe", _unsubscribe)
    monkeypatch.setattr(ha_client, "get_all_states", lambda: {"alarm_control_panel.alarmo": {"state": "disarmed"}})
    monkeypatch.setattr(ha_client, "_subscribers", set())

    app = _build_test_app()
    client = TestClient(app)

    with client.websocket_connect("/ws?api_key=test-api-key") as ws_conn:
        payload = json.loads(ws_conn.receive_text())
        assert payload["type"] == "initial_state"
        assert "states" in payload

    assert subscribed == []
