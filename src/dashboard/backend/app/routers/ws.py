"""
WebSocket endpoint /ws
Cada cliente que conecta recebe eventos em tempo real do Home Assistant.
"""

import asyncio
import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.security import require_ws_api_key
from app.services import ha_client

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await require_ws_api_key(websocket)
    await websocket.accept()
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=200)

    async def enqueue(payload: str) -> None:
        try:
            queue.put_nowait(payload)
        except asyncio.QueueFull:
            pass  # descarta mensagem se fila cheia (cliente lento)

    ha_client.subscribe(enqueue)
    logger.info("Cliente WS conectado. Total: %d", len(ha_client._subscribers))

    # Envia snapshot completo dos estados atuais ao conectar
    try:
        await websocket.send_text(
            json.dumps(
                {
                    "type": "initial_state",
                    "states": ha_client.get_all_states(),
                }
            )
        )

        while True:
            # Aguarda mensagem da fila (com timeout para detectar desconexão)
            try:
                payload = await asyncio.wait_for(queue.get(), timeout=30)
                await websocket.send_text(payload)
            except asyncio.TimeoutError:
                # Envia ping para manter conexão viva
                await websocket.send_text(json.dumps({"type": "ping"}))

    except WebSocketDisconnect:
        logger.info("Cliente WS desconectado.")
    except Exception as exc:
        logger.warning("Erro no WebSocket: %s", exc)
    finally:
        ha_client.unsubscribe(enqueue)
