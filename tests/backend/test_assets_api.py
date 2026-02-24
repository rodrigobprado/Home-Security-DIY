"""Testes de contrato da API de Cadastro de Ativos — Issues #336, #338, #339."""

import json
import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from fastapi import Depends, FastAPI

from app.db.session import get_db
from app.routers import assets as assets_router
from app.routers import audit as audit_router
from app.security import require_api_key

OPERATOR_KEY = "test-api-key"
ADMIN_KEY = "test-admin-key"
TEST_BASE_URL = "http://testserver"


# ---------------------------------------------------------------------------
# Helpers de fixtures de DB
# ---------------------------------------------------------------------------


def _make_asset(
    asset_type="sensor",
    entity_id="binary_sensor.porta",
    name="Sensor Porta",
    status="active",
    is_active=True,
) -> MagicMock:
    a = MagicMock()
    a.id = uuid.uuid4()
    a.asset_type = asset_type
    a.name = name
    a.entity_id = entity_id
    a.status = status
    a.location = "entrada"
    a.description = None
    a.config_json = None
    a.is_active = is_active
    a.created_at = datetime.now(timezone.utc)
    a.updated_at = datetime.now(timezone.utc)
    a.created_by = "test"
    a.updated_by = "test"
    return a


class _FakeScalars:
    def __init__(self, rows):
        self._rows = rows

    def all(self):
        return self._rows

    def scalar_one(self):
        return len(self._rows)

    def scalar_one_or_none(self):
        return self._rows[0] if self._rows else None


class _FakeResult:
    def __init__(self, rows):
        self._rows = rows

    def scalars(self):
        return _FakeScalars(self._rows)

    def scalar_one(self):
        return len(self._rows)

    def scalar_one_or_none(self):
        return self._rows[0] if self._rows else None


class _FakeSession:
    def __init__(self, rows=None, conflict=False):
        self._rows = rows or []
        self._conflict = conflict
        self.added = []

    async def execute(self, _stmt):
        return _FakeResult(self._rows)

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        pass

    async def commit(self):
        pass

    async def refresh(self, obj):
        pass


def _build_test_app(db_rows=None, conflict=False):
    fake_session = _FakeSession(rows=db_rows, conflict=conflict)

    async def _override_get_db():
        yield fake_session

    app = FastAPI()
    app.include_router(assets_router.router, dependencies=[Depends(require_api_key)])
    app.include_router(audit_router.router, dependencies=[Depends(require_api_key)])
    app.dependency_overrides[get_db] = _override_get_db
    return app


# ---------------------------------------------------------------------------
# Testes de autenticação (Issue #338 — RBAC)
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_list_assets_requires_operator_key():
    """GET /api/assets deve exigir X-API-Key (operator)."""
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get("/api/assets")
    assert resp.status_code == 403


@pytest.mark.anyio
async def test_list_assets_with_operator_key():
    """GET /api/assets com X-API-Key retorna 200."""
    app = _build_test_app(db_rows=[_make_asset()])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get("/api/assets", headers={"X-API-Key": OPERATOR_KEY})
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.anyio
async def test_create_asset_requires_admin_key():
    """POST /api/assets sem X-Admin-Key deve retornar 503 (admin key não configurada para teste vazio)
    ou 403 (admin key inválida)."""
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        # Sem admin key — deve falhar (apenas operator key)
        resp = await client.post(
            "/api/assets",
            headers={"X-API-Key": OPERATOR_KEY},
            json={
                "asset_type": "sensor",
                "name": "Sensor Teste",
                "entity_id": "binary_sensor.teste",
            },
        )
    assert resp.status_code in (403, 503)  # sem X-Admin-Key


@pytest.mark.anyio
async def test_create_asset_with_wrong_admin_key():
    """POST /api/assets com X-Admin-Key errada deve retornar 403."""
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.post(
            "/api/assets",
            headers={"X-API-Key": OPERATOR_KEY, "X-Admin-Key": "wrong-key"},
            json={
                "asset_type": "sensor",
                "name": "Sensor Teste",
                "entity_id": "binary_sensor.teste",
            },
        )
    assert resp.status_code == 403


@pytest.mark.anyio
async def test_delete_asset_requires_admin_key():
    """DELETE /api/assets/{id} sem X-Admin-Key deve falhar."""
    asset_id = uuid.uuid4()
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.delete(
            f"/api/assets/{asset_id}",
            headers={"X-API-Key": OPERATOR_KEY},
        )
    assert resp.status_code in (403, 503)


# ---------------------------------------------------------------------------
# Testes de CRUD (Issue #336)
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_list_assets_empty():
    """GET /api/assets sem ativos retorna lista vazia."""
    app = _build_test_app(db_rows=[])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get("/api/assets", headers={"X-API-Key": OPERATOR_KEY})
    assert resp.status_code == 200
    assert resp.json()["items"] == []


@pytest.mark.anyio
async def test_list_assets_pagination_params():
    """GET /api/assets aceita limit e offset como query params."""
    app = _build_test_app(db_rows=[_make_asset() for _ in range(3)])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get(
            "/api/assets?limit=2&offset=1",
            headers={"X-API-Key": OPERATOR_KEY},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["limit"] == 2
    assert data["offset"] == 1


@pytest.mark.anyio
async def test_get_asset_not_found():
    """GET /api/assets/{id} com ID inexistente retorna 404."""
    app = _build_test_app(db_rows=[])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get(
            f"/api/assets/{uuid.uuid4()}",
            headers={"X-API-Key": OPERATOR_KEY},
        )
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_get_asset_found():
    """GET /api/assets/{id} com ID existente retorna o ativo."""
    asset = _make_asset()
    app = _build_test_app(db_rows=[asset])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get(
            f"/api/assets/{asset.id}",
            headers={"X-API-Key": OPERATOR_KEY},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["entity_id"] == asset.entity_id
    assert data["asset_type"] == asset.asset_type


@pytest.mark.anyio
async def test_create_asset_invalid_payload():
    """POST /api/assets com payload inválido retorna 422."""
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.post(
            "/api/assets",
            headers={"X-API-Key": OPERATOR_KEY, "X-Admin-Key": ADMIN_KEY},
            json={"asset_type": "invalid_type", "name": "X", "entity_id": "test.x"},
        )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_create_asset_entity_id_with_space():
    """POST /api/assets com entity_id contendo espaço retorna 422."""
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.post(
            "/api/assets",
            headers={"X-API-Key": OPERATOR_KEY, "X-Admin-Key": ADMIN_KEY},
            json={"asset_type": "sensor", "name": "X", "entity_id": "binary sensor.teste"},
        )
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_create_asset_invalid_config_json():
    """POST /api/assets com config_json inválido retorna 422."""
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.post(
            "/api/assets",
            headers={"X-API-Key": OPERATOR_KEY, "X-Admin-Key": ADMIN_KEY},
            json={
                "asset_type": "sensor",
                "name": "Sensor",
                "entity_id": "binary_sensor.ok",
                "config_json": "not-valid-json{{{",
            },
        )
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Testes de campos de resposta (Issue #338 — sem credenciais sensíveis)
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_asset_response_has_no_sensitive_fields():
    """Resposta da API de ativos não deve expor campos sensíveis."""
    asset = _make_asset()
    app = _build_test_app(db_rows=[asset])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get(
            f"/api/assets/{asset.id}",
            headers={"X-API-Key": OPERATOR_KEY},
        )
    assert resp.status_code == 200
    data = resp.json()
    # Campos sensíveis NÃO devem aparecer na resposta
    assert "credential" not in str(data).lower()
    assert "password" not in str(data).lower()
    assert "secret" not in str(data).lower()
    # Campos esperados devem estar presentes
    assert "id" in data
    assert "asset_type" in data
    assert "entity_id" in data
    assert "name" in data
    assert "status" in data
    assert "is_active" in data


# ---------------------------------------------------------------------------
# Testes de Auditoria (Issue #339)
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_audit_list_requires_operator_key():
    """GET /api/audit deve exigir X-API-Key."""
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get("/api/audit")
    assert resp.status_code == 403


@pytest.mark.anyio
async def test_audit_list_with_operator_key():
    """GET /api/audit com X-API-Key retorna 200."""
    app = _build_test_app(db_rows=[])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get("/api/audit", headers={"X-API-Key": OPERATOR_KEY})
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.anyio
async def test_audit_export_json_format():
    """GET /api/audit/export?format=json retorna Content-Type application/json."""
    app = _build_test_app(db_rows=[])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get(
            "/api/audit/export?format=json",
            headers={"X-API-Key": OPERATOR_KEY},
        )
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("content-type", "")
    assert "attachment" in resp.headers.get("content-disposition", "")


@pytest.mark.anyio
async def test_audit_export_csv_format():
    """GET /api/audit/export?format=csv retorna Content-Type text/csv."""
    app = _build_test_app(db_rows=[])
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
        resp = await client.get(
            "/api/audit/export?format=csv",
            headers={"X-API-Key": OPERATOR_KEY},
        )
    assert resp.status_code == 200
    assert "text/csv" in resp.headers.get("content-type", "")
    assert "attachment" in resp.headers.get("content-disposition", "")
