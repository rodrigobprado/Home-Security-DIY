"""Router de Cadastro e Gestão de Ativos — Issues #336, #338, #339."""

import json
import uuid
from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Asset, AssetAudit, AssetCredential
from app.db.session import get_db
from app.security import require_admin_key

router = APIRouter(prefix="/api/assets", tags=["assets"])
ASSET_NOT_FOUND_DETAIL = "Asset not found."

# ---------------------------------------------------------------------------
# Schemas Pydantic
# ---------------------------------------------------------------------------

AssetType = Literal["sensor", "camera", "ugv", "uav"]
AssetStatus = Literal["active", "inactive", "offline", "maintenance"]


class AssetCreate(BaseModel):
    asset_type: AssetType
    name: str = Field(..., min_length=1, max_length=200)
    entity_id: str = Field(..., min_length=1, max_length=200)
    status: AssetStatus = "active"
    location: str | None = Field(default=None, max_length=200)
    description: str | None = None
    config_json: str | None = None  # JSON de configuração por tipo

    @field_validator("entity_id")
    @classmethod
    def validate_entity_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("entity_id cannot be empty.")
        if " " in value:
            raise ValueError("entity_id cannot contain spaces.")
        return value

    @field_validator("config_json")
    @classmethod
    def validate_config_json(cls, value: str | None) -> str | None:
        if value is None:
            return None
        try:
            json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError("config_json must be valid JSON.") from exc
        return value


class AssetUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    status: AssetStatus | None = None
    location: str | None = Field(default=None, max_length=200)
    description: str | None = None
    config_json: str | None = None
    is_active: bool | None = None

    @field_validator("config_json")
    @classmethod
    def validate_config_json(cls, value: str | None) -> str | None:
        if value is None:
            return None
        try:
            json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError("config_json must be valid JSON.") from exc
        return value


def _asset_to_dict(a: Asset) -> dict:
    """Serializa Asset para resposta — sem credenciais sensíveis."""
    return {
        "id": str(a.id),
        "asset_type": a.asset_type,
        "name": a.name,
        "entity_id": a.entity_id,
        "status": a.status,
        "location": a.location,
        "description": a.description,
        "config_json": a.config_json,
        "is_active": a.is_active,
        "created_at": a.created_at.isoformat() if a.created_at else None,
        "updated_at": a.updated_at.isoformat() if a.updated_at else None,
        "created_by": a.created_by,
        "updated_by": a.updated_by,
    }


def _get_actor(request: Request) -> str:
    return request.headers.get("X-Actor", "api")


def _get_actor_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def _write_audit(
    db: AsyncSession,
    *,
    asset_id: uuid.UUID | None,
    action: str,
    before: dict | None,
    after: dict | None,
    actor: str,
    actor_ip: str,
) -> None:
    audit = AssetAudit(
        asset_id=asset_id,
        action=action,
        before_json=json.dumps(before, default=str) if before else None,
        after_json=json.dumps(after, default=str) if after else None,
        actor=actor,
        actor_ip=actor_ip,
    )
    db.add(audit)


# ---------------------------------------------------------------------------
# Endpoints — leitura (require_api_key via main.py)
# ---------------------------------------------------------------------------


@router.get("", summary="Listar ativos com filtros e paginação")
async def list_assets(
    asset_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """GET /api/assets — Retorna catálogo de ativos com filtros opcionais."""
    stmt = select(Asset).order_by(desc(Asset.updated_at))
    if asset_type:
        stmt = stmt.where(Asset.asset_type == asset_type)
    if status:
        stmt = stmt.where(Asset.status == status)
    if is_active is not None:
        stmt = stmt.where(Asset.is_active == is_active)
    if search:
        like = f"%{search}%"
        stmt = stmt.where(Asset.name.ilike(like) | Asset.entity_id.ilike(like))

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    result = await db.execute(stmt.offset(offset).limit(limit))
    assets = result.scalars().all()
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "items": [_asset_to_dict(a) for a in assets],
    }


@router.get("/{asset_id}", summary="Obter ativo por ID")
async def get_asset(asset_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> dict:
    """GET /api/assets/{id} — Retorna um ativo específico."""
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ASSET_NOT_FOUND_DETAIL)
    return _asset_to_dict(asset)


# ---------------------------------------------------------------------------
# Endpoints — escrita (require_admin_key — Issue #338)
# ---------------------------------------------------------------------------


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_key)],
    summary="Criar novo ativo (admin)",
)
async def create_asset(
    payload: AssetCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """POST /api/assets — Cadastra novo ativo. Requer X-Admin-Key."""
    existing = await db.execute(select(Asset).where(Asset.entity_id == payload.entity_id))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Asset with entity_id '{payload.entity_id}' already exists.",
        )

    actor = _get_actor(request)
    actor_ip = _get_actor_ip(request)
    now = datetime.now(timezone.utc)
    asset = Asset(
        id=uuid.uuid4(),
        asset_type=payload.asset_type,
        name=payload.name,
        entity_id=payload.entity_id,
        status=payload.status,
        location=payload.location,
        description=payload.description,
        config_json=payload.config_json,
        is_active=True,
        created_at=now,
        updated_at=now,
        created_by=actor,
        updated_by=actor,
    )
    db.add(asset)
    await db.flush()  # gera id para auditoria

    await _write_audit(
        db,
        asset_id=asset.id,
        action="create",
        before=None,
        after=_asset_to_dict(asset),
        actor=actor,
        actor_ip=actor_ip,
    )
    await db.commit()
    await db.refresh(asset)
    return _asset_to_dict(asset)


@router.put(
    "/{asset_id}",
    dependencies=[Depends(require_admin_key)],
    summary="Atualizar ativo (admin)",
)
async def update_asset(
    asset_id: uuid.UUID,
    payload: AssetUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """PUT /api/assets/{id} — Atualiza campos de um ativo. Requer X-Admin-Key."""
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ASSET_NOT_FOUND_DETAIL)

    before = _asset_to_dict(asset)
    actor = _get_actor(request)
    actor_ip = _get_actor_ip(request)

    if payload.name is not None:
        asset.name = payload.name
    if payload.status is not None:
        asset.status = payload.status
    if payload.location is not None:
        asset.location = payload.location
    if payload.description is not None:
        asset.description = payload.description
    if payload.config_json is not None:
        asset.config_json = payload.config_json
    if payload.is_active is not None:
        asset.is_active = payload.is_active
    asset.updated_at = datetime.now(timezone.utc)
    asset.updated_by = actor

    await _write_audit(
        db,
        asset_id=asset.id,
        action="update",
        before=before,
        after=_asset_to_dict(asset),
        actor=actor,
        actor_ip=actor_ip,
    )
    await db.commit()
    await db.refresh(asset)
    return _asset_to_dict(asset)


@router.delete(
    "/{asset_id}",
    dependencies=[Depends(require_admin_key)],
    summary="Desativar ativo (soft delete) (admin)",
)
async def delete_asset(
    asset_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """DELETE /api/assets/{id} — Soft delete: marca is_active=False. Requer X-Admin-Key."""
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ASSET_NOT_FOUND_DETAIL)

    before = _asset_to_dict(asset)
    actor = _get_actor(request)
    actor_ip = _get_actor_ip(request)

    asset.is_active = False
    asset.status = "inactive"
    asset.updated_at = datetime.now(timezone.utc)
    asset.updated_by = actor

    await _write_audit(
        db,
        asset_id=asset.id,
        action="delete",
        before=before,
        after=_asset_to_dict(asset),
        actor=actor,
        actor_ip=actor_ip,
    )
    await db.commit()
    return {"status": "deactivated", "id": str(asset_id)}


@router.post(
    "/{asset_id}/restore",
    dependencies=[Depends(require_admin_key)],
    summary="Restaurar ativo desativado (admin)",
)
async def restore_asset(
    asset_id: uuid.UUID,
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """POST /api/assets/{id}/restore — Reativa ativo. Requer X-Admin-Key."""
    result = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ASSET_NOT_FOUND_DETAIL)

    before = _asset_to_dict(asset)
    actor = _get_actor(request)
    actor_ip = _get_actor_ip(request)

    asset.is_active = True
    asset.status = "active"
    asset.updated_at = datetime.now(timezone.utc)
    asset.updated_by = actor

    await _write_audit(
        db,
        asset_id=asset.id,
        action="restore",
        before=before,
        after=_asset_to_dict(asset),
        actor=actor,
        actor_ip=actor_ip,
    )
    await db.commit()
    await db.refresh(asset)
    return _asset_to_dict(asset)
