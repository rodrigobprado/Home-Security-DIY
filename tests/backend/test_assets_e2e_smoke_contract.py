"""Smoke tests E2E de fluxo completo do catálogo de ativos — Issue #340.

Estes testes validam o fluxo cadastro → persistência → exibição → auditoria
usando mocks de sessão para simular comportamento integrado end-to-end.
"""

import json
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from fastapi import Depends, FastAPI

from app.db.session import get_db
from app.routers import alerts, assets as assets_router, audit as audit_router
from app.security import require_api_key

OPERATOR_KEY = "test-api-key"
ADMIN_KEY = "test-admin-key"
TEST_BASE_URL = "http://testserver"
ASSETS_ENDPOINT = "/api/assets"


class _FullSmokeSession:
    """Sessão de banco que simula o estado completo do sistema em E2E."""

    def __init__(self):
        self._assets: dict[str, MagicMock] = {}
        self._audit_trail: list[MagicMock] = []
        self.flushed = []
        self.committed = []

    def _make_audit_record(self, asset_id, action, before, after, actor, actor_ip):
        record = MagicMock()
        record.id = len(self._audit_trail) + 1
        record.asset_id = asset_id
        record.action = action
        record.before_json = json.dumps(before, default=str) if before else None
        record.after_json = json.dumps(after, default=str) if after else None
        record.actor = actor
        record.actor_ip = actor_ip
        record.created_at = datetime.now(timezone.utc)
        return record

    async def execute(self, stmt):
        # Retorna resultado baseado no conteúdo da query (simplificado)
        result = MagicMock()
        scalars = MagicMock()
        scalars.all.return_value = list(self._assets.values())
        scalars.scalar_one.return_value = len(self._assets)
        scalars.scalar_one_or_none.return_value = (
            list(self._assets.values())[0] if self._assets else None
        )
        result.scalars.return_value = scalars
        result.scalar_one.return_value = len(self._assets)
        result.scalar_one_or_none.return_value = (
            list(self._assets.values())[0] if self._assets else None
        )
        return result

    def add(self, obj):
        from app.db.models import Asset, AssetAudit

        if isinstance(obj, Asset):
            self._assets[str(obj.id)] = obj
        elif isinstance(obj, AssetAudit):
            self._audit_trail.append(obj)

    async def flush(self):
        self.flushed.append(True)

    async def commit(self):
        self.committed.append(True)

    async def refresh(self, obj):
        # No-op intencional para o test double de sessão.
        return None


def _build_smoke_app():
    session = _FullSmokeSession()

    async def _override():
        yield session

    app = FastAPI()
    app.include_router(assets_router.router, dependencies=[Depends(require_api_key)])
    app.include_router(audit_router.router, dependencies=[Depends(require_api_key)])
    app.include_router(alerts.router, dependencies=[Depends(require_api_key)])
    app.dependency_overrides[get_db] = _override
    return app, session


# ---------------------------------------------------------------------------
# Fluxo completo: cadastro → auditoria
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_smoke_create_asset_generates_audit_event():
    """Smoke: criação de ativo deve gerar evento de auditoria."""
    app, session = _build_smoke_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.post(
            ASSETS_ENDPOINT,
            headers={"X-API-Key": OPERATOR_KEY, "X-Admin-Key": ADMIN_KEY},
            json={
                "asset_type": "sensor",
                "name": "Sensor Porta Smoke",
                "entity_id": "binary_sensor.porta_smoke",
                "location": "entrada",
            },
        )

    assert resp.status_code == 201
    data = resp.json()
    assert data["entity_id"] == "binary_sensor.porta_smoke"
    assert data["asset_type"] == "sensor"
    assert data["is_active"] is True

    # Verificar que foi adicionado ao "banco"
    assert len(session._assets) == 1
    # Verificar que auditoria foi gerada
    assert len(session._audit_trail) == 1
    assert session._audit_trail[0].action == "create"


@pytest.mark.anyio
async def test_smoke_asset_response_excludes_credentials():
    """Smoke: resposta de ativo nunca inclui campos sensíveis."""
    app, session = _build_smoke_app()

    # Pré-popular com um ativo
    from app.db.models import Asset
    asset = Asset(
        id=uuid.uuid4(),
        asset_type="camera",
        name="Camera Smoke",
        entity_id="camera.smoke",
        status="active",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session._assets[str(asset.id)] = asset

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get(
            f"/api/assets/{asset.id}",
            headers={"X-API-Key": OPERATOR_KEY},
        )

    assert resp.status_code == 200
    body = resp.text
    assert "credential" not in body.lower()
    assert "password" not in body.lower()
    assert "secret" not in body.lower()


@pytest.mark.anyio
async def test_smoke_soft_delete_marks_inactive():
    """Smoke: DELETE soft-delete marca is_active=False sem remover do banco."""
    app, session = _build_smoke_app()

    from app.db.models import Asset
    asset = Asset(
        id=uuid.uuid4(),
        asset_type="sensor",
        name="Sensor Para Deletar",
        entity_id="binary_sensor.para_deletar",
        status="active",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session._assets[str(asset.id)] = asset

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.delete(
            f"/api/assets/{asset.id}",
            headers={"X-API-Key": OPERATOR_KEY, "X-Admin-Key": ADMIN_KEY},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "deactivated"

    # Verificar que auditoria de delete foi gerada
    delete_audits = [a for a in session._audit_trail if a.action == "delete"]
    assert len(delete_audits) == 1


@pytest.mark.anyio
async def test_smoke_restore_reactivates_asset():
    """Smoke: restore reativa ativo desativado."""
    app, session = _build_smoke_app()

    from app.db.models import Asset
    asset = Asset(
        id=uuid.uuid4(),
        asset_type="ugv",
        name="UGV Inativo",
        entity_id="device.ugv_inativo",
        status="inactive",
        is_active=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session._assets[str(asset.id)] = asset

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.post(
            f"/api/assets/{asset.id}/restore",
            headers={"X-API-Key": OPERATOR_KEY, "X-Admin-Key": ADMIN_KEY},
        )

    assert resp.status_code == 200
    # Verificar auditoria de restore
    restore_audits = [a for a in session._audit_trail if a.action == "restore"]
    assert len(restore_audits) == 1


@pytest.mark.anyio
async def test_smoke_audit_export_returns_attachment():
    """Smoke: exportação de auditoria retorna Content-Disposition attachment."""
    app, session = _build_smoke_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        for fmt in ("json", "csv"):
            resp = await client.get(
                f"/api/audit/export?format={fmt}",
                headers={"X-API-Key": OPERATOR_KEY},
            )
            assert resp.status_code == 200, f"Falhou para format={fmt}"
            assert "attachment" in resp.headers.get("content-disposition", ""), (
                f"Content-Disposition ausente para format={fmt}"
            )


@pytest.mark.anyio
async def test_smoke_rbac_create_blocked_without_admin_key():
    """Smoke: criação de ativo bloqueada sem admin key."""
    app, session = _build_smoke_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        # Sem X-Admin-Key
        resp = await client.post(
            ASSETS_ENDPOINT,
            headers={"X-API-Key": OPERATOR_KEY},  # operator key, sem admin key
            json={
                "asset_type": "sensor",
                "name": "Sensor Não Autorizado",
                "entity_id": "binary_sensor.nao_autorizado",
            },
        )
    assert resp.status_code in (403, 503), (
        f"Esperado 403 ou 503, obteve {resp.status_code}"
    )
    # Ativo não deve ter sido criado
    assert len(session._assets) == 0


@pytest.mark.anyio
async def test_smoke_list_assets_no_auth_returns_403():
    """Smoke: listagem sem autenticação retorna 403."""
    app, session = _build_smoke_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get(ASSETS_ENDPOINT)
    assert resp.status_code == 403


@pytest.mark.anyio
async def test_smoke_audit_list_no_auth_returns_403():
    """Smoke: trilha de auditoria sem autenticação retorna 403."""
    app, session = _build_smoke_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get("/api/audit")
    assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Regressão: endpoints existentes não devem quebrar
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_smoke_no_regression_alerts_endpoint():
    """Regressão: /api/alerts continua funcionando após adição do catálogo."""
    app, session = _build_smoke_app()

    from app.db.models import Alert
    mock_alert = MagicMock(spec=Alert)
    mock_alert.id = 1
    mock_alert.timestamp = datetime.now(timezone.utc)
    mock_alert.entity_id = "binary_sensor.porta"
    mock_alert.event_type = "state_changed"
    mock_alert.old_state = "off"
    mock_alert.new_state = "on"
    mock_alert.severity = "warning"
    mock_alert.message = None

    async def _exec_alerts(stmt):
        result = MagicMock()
        scalars = MagicMock()
        scalars.all.return_value = [mock_alert]
        result.scalars.return_value = scalars
        return result

    session.execute = _exec_alerts

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get("/api/alerts", headers={"X-API-Key": OPERATOR_KEY})

    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
