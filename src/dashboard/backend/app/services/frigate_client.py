"""Cliente HTTP para o Frigate NVR."""

import logging

import httpx

from app.config import settings

_client: httpx.AsyncClient | None = None
logger = logging.getLogger(__name__)
_metrics = {
    "snapshot_failures_total": 0,
    "events_failures_total": 0,
    "stats_failures_total": 0,
}


def get_metrics() -> dict[str, int]:
    return dict(_metrics)


async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(
            timeout=5,
            limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        )
    return _client


async def close() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


async def get_snapshot(camera_name: str) -> bytes | None:
    """Retorna o último frame JPEG de uma câmera."""
    url = f"{settings.frigate_url}/api/{camera_name}/latest.jpg"
    try:
        client = await get_client()
        resp = await client.get(url)
        if resp.status_code == 200:
            return resp.content
        _metrics["snapshot_failures_total"] += 1
        logger.warning("Frigate snapshot unavailable", extra={"camera": camera_name, "status_code": resp.status_code})
    except httpx.RequestError as exc:
        _metrics["snapshot_failures_total"] += 1
        logger.warning("Frigate snapshot request failed", exc_info=True, extra={"camera": camera_name, "error": str(exc)})
    return None


async def get_events(
    camera: str | None = None,
    label: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """Retorna eventos de detecção recentes do Frigate."""
    params: dict = {"limit": limit}
    if camera:
        params["camera"] = camera
    if label:
        params["label"] = label
    try:
        client = await get_client()
        resp = await client.get(f"{settings.frigate_url}/api/events", params=params)
        if resp.status_code == 200:
            return resp.json()
        _metrics["events_failures_total"] += 1
        logger.warning(
            "Frigate events unavailable",
            extra={"camera": camera, "label": label, "status_code": resp.status_code},
        )
    except httpx.RequestError as exc:
        _metrics["events_failures_total"] += 1
        logger.warning("Frigate events request failed", exc_info=True, extra={"camera": camera, "label": label, "error": str(exc)})
    except ValueError as exc:
        _metrics["events_failures_total"] += 1
        logger.warning("Frigate events payload is not valid JSON", exc_info=True, extra={"camera": camera, "label": label, "error": str(exc)})
    return []


async def get_stats() -> dict:
    """Retorna estatísticas gerais do Frigate (detecções, FPS, etc.)."""
    try:
        client = await get_client()
        resp = await client.get(f"{settings.frigate_url}/api/stats")
        if resp.status_code == 200:
            return resp.json()
        _metrics["stats_failures_total"] += 1
        logger.warning("Frigate stats unavailable", extra={"status_code": resp.status_code})
    except httpx.RequestError as exc:
        _metrics["stats_failures_total"] += 1
        logger.warning("Frigate stats request failed", exc_info=True, extra={"error": str(exc)})
    except ValueError as exc:
        _metrics["stats_failures_total"] += 1
        logger.warning("Frigate stats payload is not valid JSON", exc_info=True, extra={"error": str(exc)})
    return {}
