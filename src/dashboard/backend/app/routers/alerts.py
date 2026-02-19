from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Alert, DevicePosition
from app.db.session import get_db

router = APIRouter(prefix="/api", tags=["alerts"])


@router.get("/alerts")
async def list_alerts(
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    severity: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[dict]:
    """Retorna histórico de alertas paginado, do mais recente para o mais antigo."""
    stmt = select(Alert).order_by(desc(Alert.timestamp)).offset(offset).limit(limit)
    if severity:
        stmt = stmt.where(Alert.severity == severity)
    result = await db.execute(stmt)
    alerts = result.scalars().all()
    return [
        {
            "id": a.id,
            "timestamp": a.timestamp.isoformat(),
            "entity_id": a.entity_id,
            "event_type": a.event_type,
            "old_state": a.old_state,
            "new_state": a.new_state,
            "severity": a.severity,
            "message": a.message,
        }
        for a in alerts
    ]


@router.get("/map/devices")
async def list_device_positions(db: AsyncSession = Depends(get_db)) -> list[dict]:
    """Retorna posições dos dispositivos no mapa operacional."""
    result = await db.execute(select(DevicePosition))
    devices = result.scalars().all()
    return [
        {
            "entity_id": d.entity_id,
            "label": d.label,
            "x": d.x,
            "y": d.y,
            "device_type": d.device_type,
        }
        for d in devices
    ]
