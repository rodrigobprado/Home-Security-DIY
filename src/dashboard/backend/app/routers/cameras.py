from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import Alert
from app.db.session import get_db
from app.services import frigate_client

router = APIRouter(prefix="/api/cameras", tags=["cameras"])


@router.get("/{camera_name}/snapshot")
async def get_snapshot(
    camera_name: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Response:
    """Retorna o último frame JPEG de uma câmera via Frigate."""
    if camera_name not in settings.cameras:
        raise HTTPException(status_code=404, detail=f"Câmera '{camera_name}' não encontrada.")
    data = await frigate_client.get_snapshot(camera_name)
    if data is None:
        raise HTTPException(status_code=503, detail=f"Câmera '{camera_name}' indisponível.")
    await _log_camera_access(
        db=db,
        camera_name=camera_name,
        action="snapshot",
        client_ip=request.client.host if request.client else "unknown",
    )
    return Response(content=data, media_type="image/jpeg")


@router.get("/events")
async def get_events(
    request: Request,
    camera: str | None = None,
    label: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Retorna eventos de detecção recentes do Frigate."""
    if camera and camera not in settings.cameras:
        raise HTTPException(status_code=400, detail=f"Câmera inválida: '{camera}'.")
    await _log_camera_access(
        db=db,
        camera_name=camera or "all",
        action="events",
        client_ip=request.client.host if request.client else "unknown",
    )
    return await frigate_client.get_events(camera=camera, label=label, limit=limit)


async def _log_camera_access(
    db: AsyncSession,
    camera_name: str,
    action: str,
    client_ip: str,
) -> None:
    """LGPD/CFTV: registro de acesso operacional às câmeras e eventos."""
    entry = Alert(
        timestamp=datetime.now(timezone.utc),
        entity_id=f"camera.{camera_name}",
        event_type="camera_access",
        old_state=None,
        new_state=action,
        severity="info",
        message=f"camera_access action={action} camera={camera_name} ip={client_ip}",
    )
    db.add(entry)
    await db.commit()
