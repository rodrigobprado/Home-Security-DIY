import json
from datetime import datetime
from typing import ClassVar

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, field_validator
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Alert, Asset, DashboardConfig, DevicePosition
from app.db.session import get_db
from app.security import require_admin_key

router = APIRouter(prefix="/api", tags=["alerts"])
MAP_FLOORPLAN_IMAGE_KEY = "map.floorplan_image_data_url"
MAP_GEO_BOUNDS_KEY = "map.geo_bounds_json"


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
    """Retorna posições dos dispositivos no mapa operacional.

    Prioriza o catálogo dinâmico de ativos (dashboard.assets).
    Fallback para device_positions legadas se catálogo estiver vazio.
    """
    # Tenta catálogo dinâmico de ativos
    assets_result = await db.execute(
        select(Asset).where(Asset.is_active == True)  # noqa: E712
    )
    assets = assets_result.scalars().all()

    if assets:
        return [
            {
                "entity_id": a.entity_id,
                "label": a.name,
                "x": 50.0,  # posição padrão; ajustável via device_positions
                "y": 50.0,
                "device_type": a.asset_type if a.asset_type in ("camera", "sensor") else "drone",
                "asset_id": str(a.id),
                "asset_type": a.asset_type,
                "status": a.status,
            }
            for a in assets
        ]

    # Fallback: device_positions legadas
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
    keys = [MAP_FLOORPLAN_IMAGE_KEY, MAP_GEO_BOUNDS_KEY]
    result = await db.execute(select(DashboardConfig).where(DashboardConfig.key.in_(keys)))
    rows = {row.key: row.value for row in result.scalars().all()}
    geo_bounds_raw = rows.get(MAP_GEO_BOUNDS_KEY)
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
        "floorplan_image_data_url": rows.get(MAP_FLOORPLAN_IMAGE_KEY),
        "geo_bounds": geo_bounds,
    }


@router.put("/map/config")
async def upsert_map_config(
    payload: MapConfigPayload,
    _admin: None = Depends(require_admin_key),
    db: AsyncSession = Depends(get_db),
) -> dict:
    if payload.floorplan_image_data_url is not None:
        await db.merge(
            DashboardConfig(
                key=MAP_FLOORPLAN_IMAGE_KEY,
                value=payload.floorplan_image_data_url,
            )
        )
    if payload.geo_bounds is not None:
        await db.merge(
            DashboardConfig(
                key=MAP_GEO_BOUNDS_KEY,
                value=json.dumps(payload.geo_bounds, separators=(",", ":"), ensure_ascii=True),
            )
        )
    await db.commit()
    return {"status": "ok"}
