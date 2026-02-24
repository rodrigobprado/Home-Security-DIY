"""Router de Trilha de Auditoria — Issue #339."""

import csv
import io
import json
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AssetAudit
from app.db.session import get_db

router = APIRouter(prefix="/api/audit", tags=["audit"])


def _audit_to_dict(a: AssetAudit) -> dict:
    return {
        "id": a.id,
        "asset_id": str(a.asset_id) if a.asset_id else None,
        "action": a.action,
        "before_json": a.before_json,
        "after_json": a.after_json,
        "actor": a.actor,
        "actor_ip": a.actor_ip,
        "created_at": a.created_at.isoformat() if a.created_at else None,
    }


@router.get("", summary="Consultar trilha de auditoria com filtros")
async def list_audit(
    asset_id: uuid.UUID | None = Query(default=None),
    action: str | None = Query(default=None, description="create|update|delete|restore"),
    actor: str | None = Query(default=None),
    since: datetime | None = Query(default=None, description="ISO 8601 — data inicial"),
    until: datetime | None = Query(default=None, description="ISO 8601 — data final"),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """GET /api/audit — Retorna trilha de auditoria paginada com filtros opcionais."""
    stmt = select(AssetAudit).order_by(desc(AssetAudit.created_at))

    if asset_id:
        stmt = stmt.where(AssetAudit.asset_id == asset_id)
    if action:
        stmt = stmt.where(AssetAudit.action == action)
    if actor:
        stmt = stmt.where(AssetAudit.actor == actor)
    if since:
        stmt = stmt.where(AssetAudit.created_at >= since)
    if until:
        stmt = stmt.where(AssetAudit.created_at <= until)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    result = await db.execute(stmt.offset(offset).limit(limit))
    records = result.scalars().all()
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "items": [_audit_to_dict(r) for r in records],
    }


@router.get("/export", summary="Exportar trilha de auditoria (CSV ou JSON)")
async def export_audit(
    format: str = Query(default="json", description="json ou csv"),
    asset_id: uuid.UUID | None = Query(default=None),
    action: str | None = Query(default=None),
    actor: str | None = Query(default=None),
    since: datetime | None = Query(default=None),
    until: datetime | None = Query(default=None),
    limit: int = Query(default=1000, ge=1, le=5000),
    db: AsyncSession = Depends(get_db),
) -> Response:
    """GET /api/audit/export — Exporta registros de auditoria em CSV ou JSON."""
    stmt = select(AssetAudit).order_by(desc(AssetAudit.created_at))

    if asset_id:
        stmt = stmt.where(AssetAudit.asset_id == asset_id)
    if action:
        stmt = stmt.where(AssetAudit.action == action)
    if actor:
        stmt = stmt.where(AssetAudit.actor == actor)
    if since:
        stmt = stmt.where(AssetAudit.created_at >= since)
    if until:
        stmt = stmt.where(AssetAudit.created_at <= until)

    result = await db.execute(stmt.limit(limit))
    records = [_audit_to_dict(r) for r in result.scalars().all()]

    if format.lower() == "csv":
        output = io.StringIO()
        if records:
            writer = csv.DictWriter(output, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
        content = output.getvalue()
        return Response(
            content=content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=audit_export.csv"},
        )

    content = json.dumps(records, ensure_ascii=False, indent=2)
    return Response(
        content=content,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=audit_export.json"},
    )
