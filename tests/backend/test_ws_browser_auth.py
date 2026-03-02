from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers import ws
from app.services import ha_client


def test_ws_allows_browser_token_query(monkeypatch):
    app = FastAPI()
    app.include_router(ws.router)

    monkeypatch.setattr(ha_client, "subscribe", lambda _cb: None)
    monkeypatch.setattr(ha_client, "unsubscribe", lambda _cb: None)
    monkeypatch.setattr(ha_client, "get_ws_metrics", lambda: {"connected_clients": 0})
    monkeypatch.setattr(ha_client, "get_all_states", lambda: {})

    with TestClient(app) as client:
        with client.websocket_connect("/ws?token=test-api-key") as socket:
            payload = socket.receive_json()
            assert payload["type"] == "initial_state"
