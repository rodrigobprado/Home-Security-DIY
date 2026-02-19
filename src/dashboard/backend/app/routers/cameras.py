from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.services import frigate_client

router = APIRouter(prefix="/api/cameras", tags=["cameras"])


@router.get("/{camera_name}/snapshot")
async def get_snapshot(camera_name: str) -> Response:
    """Retorna o último frame JPEG de uma câmera via Frigate."""
    data = await frigate_client.get_snapshot(camera_name)
    if data is None:
        raise HTTPException(status_code=503, detail=f"Câmera '{camera_name}' indisponível.")
    return Response(content=data, media_type="image/jpeg")


@router.get("/events")
async def get_events(
    camera: str | None = None,
    label: str | None = None,
    limit: int = 20,
) -> list[dict]:
    """Retorna eventos de detecção recentes do Frigate."""
    return await frigate_client.get_events(camera=camera, label=label, limit=limit)
