"""
Cliente WebSocket permanente para o Home Assistant.
Mantém uma única conexão, subscreve eventos state_changed e faz fan-out
para todos os clientes WebSocket do dashboard conectados.
Reconexão automática com backoff exponencial.

IMPORTANTE: este módulo mantém estado global em memória de processo.
A API deve rodar com apenas 1 worker de aplicação.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any

import httpx
import websockets
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import Alert
from app.db.session import AsyncSessionLocal

logger = logging.getLogger(__name__)

# Conjunto de callbacks registrados (um por cliente WS conectado ao dashboard)
_subscribers: set = set()

# Último estado conhecido de cada entidade (cache em memória)
_entity_states: dict[str, dict] = {}


def subscribe(callback) -> None:
    _subscribers.add(callback)


def unsubscribe(callback) -> None:
    _subscribers.discard(callback)


def get_all_states() -> dict[str, dict]:
    return dict(_entity_states)


def get_state(entity_id: str) -> dict | None:
    return _entity_states.get(entity_id)


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
        except Exception:
            dead.add(cb)
    _subscribers.difference_update(dead)


async def _fetch_initial_states() -> None:
    """Busca todos os estados via REST API na inicialização."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{settings.ha_url}/api/states",
                headers={"Authorization": f"Bearer {settings.ha_token}"},
            )
            if resp.status_code == 200:
                for state in resp.json():
                    _entity_states[state["entity_id"]] = state
                logger.info("Estados iniciais carregados: %d entidades", len(_entity_states))
    except Exception as exc:
        logger.warning("Não foi possível carregar estados iniciais: %s", exc)


async def run_forever() -> None:
    """Loop principal de conexão ao HA WebSocket com reconexão automática."""
    await _fetch_initial_states()

    ws_url = settings.ha_url.replace("http://", "ws://").replace("https://", "wss://")
    ws_url = f"{ws_url}/api/websocket"
    msg_id = 1
    backoff = 1

    while True:
        try:
            logger.info("Conectando ao HA WebSocket: %s", ws_url)
            async with websockets.connect(ws_url, ping_interval=30) as ws:
                backoff = 1  # reset após conexão bem-sucedida

                # 1. Autenticação
                auth_required = json.loads(await ws.recv())
                if auth_required.get("type") == "auth_required":
                    await ws.send(
                        json.dumps({"type": "auth", "access_token": settings.ha_token})
                    )
                    auth_ok = json.loads(await ws.recv())
                    if auth_ok.get("type") != "auth_ok":
                        logger.error("Falha na autenticação HA: %s", auth_ok)
                        await asyncio.sleep(backoff)
                        backoff = min(backoff * 2, 60)
                        continue
                    logger.info("Autenticado no Home Assistant")

                # 2. Subscrever state_changed
                await ws.send(
                    json.dumps(
                        {
                            "id": msg_id,
                            "type": "subscribe_events",
                            "event_type": "state_changed",
                        }
                    )
                )
                msg_id += 1

                # 3. Loop de recebimento
                async for raw in ws:
                    msg: dict[str, Any] = json.loads(raw)
                    if msg.get("type") != "event":
                        continue

                    event = msg.get("event", {})
                    data = event.get("data", {})
                    entity_id = data.get("entity_id", "")
                    new_state_obj = data.get("new_state") or {}
                    old_state_obj = data.get("old_state") or {}

                    new_state = new_state_obj.get("state", "")
                    old_state = old_state_obj.get("state", "")

                    # Atualiza cache
                    if new_state_obj:
                        _entity_states[entity_id] = new_state_obj

                    # Persiste alertas relevantes
                    await _persist_alert(entity_id, old_state, new_state)

                    # Fan-out para clientes do dashboard
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

        except (websockets.exceptions.ConnectionClosed, OSError, asyncio.TimeoutError) as exc:
            logger.warning("Conexão HA perdida: %s. Reconectando em %ds…", exc, backoff)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
        except Exception as exc:
            logger.error("Erro inesperado no cliente HA: %s", exc, exc_info=True)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
