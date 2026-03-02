import httpx
from fastapi import APIRouter
import logging

from app.config import settings
from app.services import frigate_client, ha_client

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/services", tags=["services"])

SERVICES_TO_CHECK = {
    "home_assistant": f"{settings.ha_url}/api/",
    "frigate": f"{settings.frigate_url}/api/stats",
}

_client: httpx.AsyncClient | None = None
_metrics = {
    "status_check_failures_total": 0,
}


async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=3,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
    return _client


async def close() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def _check_http(url: str) -> str:
    try:
        client = await get_client()
        resp = await client.get(
            url,
            headers={"Authorization": f"Bearer {settings.ha_token}"}
            if url.startswith(settings.ha_url)
            else {},
        )
        return "online" if resp.status_code < 500 else "degraded"
    except (httpx.RequestError, httpx.TimeoutException) as exc:
        _metrics["status_check_failures_total"] += 1
        logger.warning("Service status check failed", exc_info=True, extra={"url": url, "error": str(exc)})
        return "offline"


@router.get("/status")
async def services_status() -> dict:
    """Verifica o status dos principais serviços do sistema."""
    results: dict[str, str] = {}
    for name, url in SERVICES_TO_CHECK.items():
        results[name] = await _check_http(url)

    # HA WebSocket connectivity (via cache de estados)
    results["ha_websocket"] = "online" if ha_client.get_all_states() else "connecting"

    return {"services": results}


@router.get("/ws-metrics")
async def ws_metrics() -> dict:
    """Retorna métricas operacionais do fan-out WebSocket."""
    return {
        "ws_metrics": ha_client.get_ws_metrics(),
        "integration_metrics": {
            "services_router": dict(_metrics),
            "frigate_client": frigate_client.get_metrics(),
        },
    }
