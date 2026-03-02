import httpx
import pytest
from fastapi import Depends, FastAPI

from app.config import settings
from app.db.session import get_db
from app.routers import alerts
from app.security import require_api_key

TEST_BASE_URL = "http://testserver"


class _FakeResult:
    def scalars(self):
        return self

    def all(self):
        return []


class _FakeSession:
    async def execute(self, _stmt):
        return _FakeResult()

    async def merge(self, _obj):
        return None

    async def commit(self):
        return None


async def _override_get_db():
    yield _FakeSession()


def _build_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(alerts.router, dependencies=[Depends(require_api_key)])
    app.dependency_overrides[get_db] = _override_get_db
    return app


@pytest.mark.anyio
async def test_put_map_config_requires_admin_key_when_configured():
    previous = settings.dashboard_admin_key
    settings.dashboard_admin_key = "test-admin-key"
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)

    try:
        async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
            resp = await client.put(
                "/api/map/config",
                headers={"X-API-Key": "test-api-key"},
                json={"geo_bounds": {"min_lat": -1, "max_lat": 1, "min_lon": -1, "max_lon": 1}},
            )
        assert resp.status_code == 403
    finally:
        settings.dashboard_admin_key = previous


@pytest.mark.anyio
async def test_put_map_config_returns_503_when_admin_key_not_configured():
    previous = settings.dashboard_admin_key
    settings.dashboard_admin_key = ""
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)

    try:
        async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
            resp = await client.put(
                "/api/map/config",
                headers={"X-API-Key": "test-api-key"},
                json={"geo_bounds": {"min_lat": -1, "max_lat": 1, "min_lon": -1, "max_lon": 1}},
            )
        assert resp.status_code == 503
    finally:
        settings.dashboard_admin_key = previous


@pytest.mark.anyio
async def test_put_map_config_allows_admin_key():
    previous = settings.dashboard_admin_key
    settings.dashboard_admin_key = "test-admin-key"
    app = _build_test_app()
    transport = httpx.ASGITransport(app=app)

    try:
        async with httpx.AsyncClient(transport=transport, base_url=TEST_BASE_URL) as client:
            resp = await client.put(
                "/api/map/config",
                headers={
                    "X-API-Key": "test-api-key",
                    "X-Admin-Key": "test-admin-key",
                },
                json={"geo_bounds": {"min_lat": -1, "max_lat": 1, "min_lon": -1, "max_lon": 1}},
            )
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
    finally:
        settings.dashboard_admin_key = previous
