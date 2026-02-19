"""Cliente HTTP para o Frigate NVR."""

import httpx

from app.config import settings


async def get_snapshot(camera_name: str) -> bytes | None:
    """Retorna o último frame JPEG de uma câmera."""
    url = f"{settings.frigate_url}/api/{camera_name}/latest.jpg"
    try:
        async with httpx.AsyncClient(timeout=5) as client:
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
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{settings.frigate_url}/api/events", params=params)
            if resp.status_code == 200:
                return resp.json()
    except httpx.RequestError:
        pass
    return []


async def get_stats() -> dict:
    """Retorna estatísticas gerais do Frigate (detecções, FPS, etc.)."""
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(f"{settings.frigate_url}/api/stats")
            if resp.status_code == 200:
                return resp.json()
    except httpx.RequestError:
        pass
    return {}
