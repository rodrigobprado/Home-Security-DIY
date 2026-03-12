"""
Cliente de estado Home Assistant via MQTT.
Subscreve ao tópico alimentado pelo ha-worker, mantém cache em memória
e faz fan-out para clientes WebSocket do dashboard.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any

import httpx
import aiomqtt
from app.config import settings
from app.db.models import Alert
from app.db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)

# Conjunto de callbacks registrados (um por cliente WS conectado ao dashboard)
_subscribers: set = set()

# Último estado conhecido de cada entidade (cache em memória)
_entity_states: dict[str, dict] = {}
_rest_client: httpx.AsyncClient | None = None
_metrics = {
    "messages_dropped_total": 0,
    "messages_fanout_total": 0,
    "fanout_failures_total": 0,
    "ws_handler_failures_total": 0,
    "initial_state_fetch_failures_total": 0,
    "event_decode_failures_total": 0,
    "unexpected_errors_total": 0,
}

MQTT_TOPIC = "home-security/ha/state_changed"


async def _get_rest_client() -> httpx.AsyncClient:
    global _rest_client
    if _rest_client is None:
        _rest_client = httpx.AsyncClient(
            timeout=10,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
    return _rest_client


async def close() -> None:
    global _rest_client
    if _rest_client is not None:
        await _rest_client.aclose()
        _rest_client = None


def subscribe(callback) -> None:
    _subscribers.add(callback)


def unsubscribe(callback) -> None:
    _subscribers.discard(callback)


def get_all_states() -> dict[str, dict]:
    return dict(_entity_states)


def get_state(entity_id: str) -> dict | None:
    return _entity_states.get(entity_id)


def record_ws_drop() -> None:
    _metrics["messages_dropped_total"] += 1


def get_ws_metrics() -> dict[str, int]:
    return {
        **_metrics,
        "connected_clients": len(_subscribers),
    }


def record_ws_handler_failure() -> None:
    _metrics["ws_handler_failures_total"] += 1


def _severity_for(entity_id: str, new_state: str) -> str:
    """Determina severidade de um evento com base na entidade e estado."""
    if entity_id == "alarm_control_panel.alarmo":
        if new_state == "triggered":
            return "critical"
        if new_state.startswith("armed"):
            return "warning"
    if entity_id.startswith("binary_sensor.") and new_state == "on":
        return "warning"
    return "info"


async def _persist_alert(entity_id: str, old_state: str, new_state: str) -> None:
    """Salva alertas relevantes no PostgreSQL."""
    if entity_id not in settings.alert_entities:
        return
    severity = _severity_for(entity_id, new_state)
    if severity == "info" and old_state == new_state:
        return

    async with AsyncSessionLocal() as session:
        alert = Alert(
            timestamp=datetime.now(timezone.utc),
            entity_id=entity_id,
            event_type="state_changed",
            old_state=old_state,
            new_state=new_state,
            severity=severity,
            message=f"{entity_id}: {old_state} → {new_state}",
        )
        session.add(alert)
        await session.commit()


async def _fan_out(message: dict) -> None:
    """Envia mensagem para todos os clientes WS do dashboard."""
    dead = set()
    payload = json.dumps(message)
    for cb in list(_subscribers):
        try:
            await cb(payload)
            _metrics["messages_fanout_total"] += 1
        except (RuntimeError, ValueError, TypeError) as exc:
            _metrics["fanout_failures_total"] += 1
            logger.warning("Falha no fan-out para cliente WS", exc_info=True, extra={"error": str(exc)})
            dead.add(cb)
    _subscribers.difference_update(dead)


async def _fetch_initial_states() -> None:
    """Busca todos os estados via REST API na inicialização."""
    try:
        client = await _get_rest_client()
        resp = await client.get(
            f"{settings.ha_url}/api/states",
            headers={"Authorization": f"Bearer {settings.ha_token}"},
        )
        if resp.status_code != 200:
            _metrics["initial_state_fetch_failures_total"] += 1
            logger.warning(
                "Não foi possível carregar estados iniciais",
                extra={"status_code": resp.status_code},
            )
            return
        for state in resp.json():
            _entity_states[state["entity_id"]] = state
        logger.info("Estados iniciais carregados: %d entidades", len(_entity_states))
    except httpx.RequestError as exc:
        _metrics["initial_state_fetch_failures_total"] += 1
        logger.warning("Erro de rede ao carregar estados iniciais", exc_info=True, extra={"error": str(exc)})
    except ValueError as exc:
        _metrics["initial_state_fetch_failures_total"] += 1
        logger.warning("Payload inválido ao carregar estados iniciais", exc_info=True, extra={"error": str(exc)})


async def _process_event_message(msg: dict[str, Any]) -> None:
    event = msg.get("event", {})
    data = event.get("data", {})
    entity_id = data.get("entity_id", "")
    new_state_obj = data.get("new_state") or {}
    old_state_obj = data.get("old_state") or {}

    new_state = new_state_obj.get("state", "")
    old_state = old_state_obj.get("state", "")

    if new_state_obj:
        _entity_states[entity_id] = new_state_obj

    await _persist_alert(entity_id, old_state, new_state)
    await _fan_out(
        {
            "type": "state_changed",
            "entity_id": entity_id,
            "old_state": old_state,
            "new_state": new_state,
            "attributes": new_state_obj.get("attributes", {}),
            "last_changed": new_state_obj.get("last_changed"),
        }
    )


async def run_forever() -> None:
    """Consome eventos do HA worker via MQTT."""
    await _fetch_initial_states()

    backoff = 1
    while True:
        try:
            async with aiomqtt.Client(
                hostname=settings.mqtt_broker,
                port=settings.mqtt_port,
                username=settings.mqtt_user,
                password=settings.mqtt_password,
            ) as client:
                logger.info("Subscrito ao tópico MQTT de estados HA: %s", MQTT_TOPIC)
                await client.subscribe(MQTT_TOPIC)
                backoff = 1
                async for message in client.messages:
                    try:
                        msg = json.loads(message.payload.decode())
                        await _process_event_message(msg)
                    except json.JSONDecodeError:
                        _metrics["event_decode_failures_total"] += 1
                        logger.warning("JSON inválido no MQTT HA")

        except aiomqtt.MqttError as exc:
            logger.warning("Conexão MQTT HA perdida: %s. Reconectando em %ds…", exc, backoff)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
        except Exception as exc:
            _metrics["unexpected_errors_total"] += 1
            logger.error("Erro inesperado no cliente HA MQTT", exc_info=True)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
