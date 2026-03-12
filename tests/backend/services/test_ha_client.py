import json
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from app.services import ha_client
from app.config import settings

@pytest.mark.anyio
async def test_ha_client_fetch_initial_states():
    # Mocking httpx.AsyncClient.get
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [
        {"entity_id": "sensor.test", "state": "on"}
    ]
    
    with patch("httpx.AsyncClient.get", return_value=mock_resp):
        await ha_client._fetch_initial_states()
        
    assert ha_client.get_state("sensor.test") == {"entity_id": "sensor.test", "state": "on"}

@pytest.mark.anyio
async def test_ha_client_authenticate_success():
    mock_ws = AsyncMock()
    # auth_required -> auth_ok
    mock_ws.recv.side_effect = [
        json.dumps({"type": "auth_required"}),
        json.dumps({"type": "auth_ok"})
    ]
    
    with patch("app.config.settings.ha_token", "test_token"):
        result = await ha_client._authenticate(mock_ws)
        
    assert result is True
    # Verify we sent the auth message
    mock_ws.send.assert_called_with(json.dumps({"type": "auth", "access_token": "test_token"}))

@pytest.mark.anyio
async def test_ha_client_authenticate_failure():
    mock_ws = AsyncMock()
    # auth_required -> auth_invalid
    mock_ws.recv.side_effect = [
        json.dumps({"type": "auth_required"}),
        json.dumps({"type": "auth_invalid", "message": "Invalid token"})
    ]
    
    result = await ha_client._authenticate(mock_ws)
    assert result is False

@pytest.mark.anyio
async def test_ha_client_process_event_message():
    msg = {
        "type": "event",
        "event": {
            "data": {
                "entity_id": "binary_sensor.test",
                "new_state": {"entity_id": "binary_sensor.test", "state": "on"},
                "old_state": {"entity_id": "binary_sensor.test", "state": "off"}
            }
        }
    }
    
    # Mock _persist_alert to avoid DB calls in unit test
    with patch("app.services.ha_client._persist_alert", new_callable=AsyncMock):
        with patch("app.services.ha_client._fan_out", new_callable=AsyncMock) as mock_fanout:
            await ha_client._process_event_message(msg)
            
            assert ha_client.get_state("binary_sensor.test") == {"entity_id": "binary_sensor.test", "state": "on"}
            mock_fanout.assert_called_once()

@pytest.mark.anyio
async def test_ha_client_subscribe_callback():
    callback = AsyncMock()
    ha_client.subscribe(callback)
    
    msg = {"type": "state_changed", "entity_id": "sensor.test", "new_state": "on"}
    await ha_client._fan_out(msg)
    
    callback.assert_called_once()
    ha_client.unsubscribe(callback)
    
    # Second fanout after unsubscribe
    await ha_client._fan_out(msg)
    # Call count should still be 1
    assert callback.call_count == 1
