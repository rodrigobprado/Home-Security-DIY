from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db.models import Asset, CameraAccessLog
from app.db.session import get_db
from app.services import frigate_client
from app.security import require_api_key, _get_request_ip

router = APIRouter(prefix="/api/cameras", tags=["cameras"])


async def _verify_camera_exists(db: AsyncSession, camera_name: str) -> bool:
    """Verifica se a câmera existe no catálogo de ativos (Assets)."""
    stmt = select(Asset).where(
        Asset.asset_type == "camera",
        Asset.entity_id == camera_name,
        Asset.is_active == True
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None


@router.get("/{camera_name}/snapshot")
async def get_snapshot(
    camera_name: str,
    request: Request,
    actor: str = Depends(require_api_key),
    db: AsyncSession = Depends(get_db),
) -> Response:
    """Retorna o último frame JPEG de uma câmera via Frigate."""
    if not await _verify_camera_exists(db, camera_name):
        raise HTTPException(status_code=404, detail=f"Câmera '{camera_name}' não encontrada ou inativa.")
    
    data = await frigate_client.get_snapshot(camera_name)
    if data is None:
        raise HTTPException(status_code=503, detail=f"Câmera '{camera_name}' indisponível no Frigate.")
    
    await _log_camera_access(
        db=db,
        camera_name=camera_name,
        action="snapshot",
        actor=actor,
        client_ip=_get_request_ip(request),
    )
    return Response(content=data, media_type="image/jpeg")


@router.get("/events")
async def get_events(
    request: Request,
    actor: str = Depends(require_api_key),
    camera: str | None = None,
    label: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Retorna eventos de detecção recentes do Frigate."""
    if camera and not await _verify_camera_exists(db, camera):
        raise HTTPException(status_code=400, detail=f"Câmera inválida ou inativa: '{camera}'.")
    
    await _log_camera_access(
        db=db,
        camera_name=camera or "all",
        action="events",
        actor=actor,
        client_ip=_get_request_ip(request),
    )
    return await frigate_client.get_events(camera=camera, label=label, limit=limit)


async def _log_camera_access(
    db: AsyncSession,
    camera_name: str,
    action: str,
    actor: str,
    client_ip: str,
) -> None:
    """LGPD/CFTV: registro de acesso operacional às câmeras em tabela dedicada."""
    entry = CameraAccessLog(
        timestamp=datetime.now(timezone.utc),
        camera_name=camera_name,
        action=action,
        actor=actor,
        client_ip=client_ip,
    )
    db.add(entry)
    await db.commit()
