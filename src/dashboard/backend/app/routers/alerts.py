import json
from datetime import datetime
from typing import ClassVar

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, field_validator
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Alert, DashboardConfig, DevicePosition
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


class MapConfigPayload(BaseModel):
    MAX_FLOORPLAN_DATA_URL_LENGTH: ClassVar[int] = 2_000_000
    floorplan_image_data_url: str | None = None
    geo_bounds: dict[str, float] | None = None

    @field_validator("floorplan_image_data_url")
    @classmethod
    def validate_floorplan_data_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if len(value) > cls.MAX_FLOORPLAN_DATA_URL_LENGTH:
            raise ValueError("floorplan image payload exceeds maximum allowed size.")
        if not value.startswith("data:image/"):
            raise ValueError("floorplan image must use data:image/* base64 format.")
        if ";base64," not in value:
            raise ValueError("floorplan image must be base64 encoded data URL.")
        return value


@router.get("/map/config")
async def get_map_config(db: AsyncSession = Depends(get_db)) -> dict:
    keys = ["map.floorplan_image_data_url", "map.geo_bounds_json"]
    result = await db.execute(select(DashboardConfig).where(DashboardConfig.key.in_(keys)))
    rows = {row.key: row.value for row in result.scalars().all()}
    geo_bounds_raw = rows.get("map.geo_bounds_json")
    geo_bounds = (
        json.loads(geo_bounds_raw)
        if geo_bounds_raw
        else {
            "min_lat": -23.5515,
            "max_lat": -23.5495,
            "min_lon": -46.6345,
            "max_lon": -46.6320,
        }
    )
    return {
        "floorplan_image_data_url": rows.get("map.floorplan_image_data_url"),
        "geo_bounds": geo_bounds,
    }


@router.put("/map/config")
async def upsert_map_config(payload: MapConfigPayload, db: AsyncSession = Depends(get_db)) -> dict:
    if payload.floorplan_image_data_url is not None:
        await db.merge(
            DashboardConfig(
                key="map.floorplan_image_data_url",
                value=payload.floorplan_image_data_url,
            )
        )
    if payload.geo_bounds is not None:
        await db.merge(
            DashboardConfig(
                key="map.geo_bounds_json",
                value=json.dumps(payload.geo_bounds, separators=(",", ":"), ensure_ascii=True),
            )
        )
    await db.commit()
    return {"status": "ok"}
