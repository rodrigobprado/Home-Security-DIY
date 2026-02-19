"""Cliente HTTP para o Frigate NVR."""

import httpx

from app.config import settings

_client: httpx.AsyncClient | None = None


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
    except httpx.RequestError:
        pass
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
    except httpx.RequestError:
        pass
    return []


async def get_stats() -> dict:
    """Retorna estatísticas gerais do Frigate (detecções, FPS, etc.)."""
    try:
        client = await get_client()
        resp = await client.get(f"{settings.frigate_url}/api/stats")
        if resp.status_code == 200:
            return resp.json()
    except httpx.RequestError:
        pass
    return {}
