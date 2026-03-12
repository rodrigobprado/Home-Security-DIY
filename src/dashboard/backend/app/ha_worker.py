import asyncio
import json
import logging
import signal
from typing import Any

import aiomqtt
import websockets
from app.config import settings
from app.utils.logging_utils import mask_url

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ha-worker")

MQTT_TOPIC = "home-security/ha/state_changed"

async def _authenticate(ws: Any) -> bool:
    try:
        raw = await ws.recv()
        auth_required = json.loads(raw)
        if auth_required.get("type") != "auth_required":
            return True

        await ws.send(json.dumps({"type": "auth", "access_token": settings.ha_token}))
        raw = await ws.recv()
        auth_ok = json.loads(raw)
        if auth_ok.get("type") != "auth_ok":
            logger.error("Falha na autenticação HA: %s", auth_ok)
            return False

        logger.info("Autenticado no Home Assistant")
        return True
    except Exception as exc:
        logger.error("Erro durante autenticação HA", exc_info=True)
        return False

async def _subscribe_state_changed(ws: Any, msg_id: int) -> int:
    await ws.send(
        json.dumps(
            {
                "id": msg_id,
                "type": "subscribe_events",
                "event_type": "state_changed",
            }
        )
    )
    return msg_id + 1

async def run_worker():
    ws_url = settings.ha_url.replace("http://", "ws://").replace("https://", "wss://") + "/api/websocket"
    msg_id = 1
    backoff = 1

    logger.info("Iniciando HA Worker...")

    while True:
        try:
            async with aiomqtt.Client(
                hostname=settings.mqtt_broker,
                port=settings.mqtt_port,
                username=settings.mqtt_user,
                password=settings.mqtt_password,
            ) as mqtt_client:
                logger.info("Conectado ao broker MQTT: %s", settings.mqtt_broker)
                
                logger.info("Conectando ao HA WebSocket: %s", mask_url(ws_url))
                async with websockets.connect(ws_url, ping_interval=30) as ws:
                    if not await _authenticate(ws):
                        await asyncio.sleep(5)
                        continue
                    
                    msg_id = await _subscribe_state_changed(ws, msg_id)
                    backoff = 1
                    
                    async for raw in ws:
                        msg = json.loads(raw)
                        if msg.get("type") == "event":
                            # Encaminha o evento para o MQTT
                            await mqtt_client.publish(
                                MQTT_TOPIC,
                                payload=json.dumps(msg),
                                qos=1
                            )

        except (websockets.exceptions.ConnectionClosed, OSError, aiomqtt.MqttError) as exc:
            logger.warning("Conexão perdida (%s). Reconectando em %ds...", type(exc).__name__, backoff)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
        except Exception as exc:
            logger.error("Erro inesperado no worker", exc_info=True)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Graceful shutdown
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: loop.stop())

    try:
        loop.run_until_complete(run_worker())
    except asyncio.CancelledError:
        pass
    finally:
        loop.close()
