"""Testes unitários focados em cobertura de branches do router de assets."""

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.config import settings
from app.db.models import Asset
from app.routers.assets import (
    AssetCreate,
    AssetUpdate,
    _forwarded_chain,
    _get_actor_ip,
    create_asset,
    delete_asset,
    list_assets,
    restore_asset,
    update_asset,
)


@dataclass
class _Result:
    one: int | None = None
    one_or_none: object | None = None
    all_rows: list | None = None

    def scalar_one(self):
        return self.one

    def scalar_one_or_none(self):
        return self.one_or_none

    def scalars(self):
        return self

    def all(self):
        return self.all_rows or []


class _DbQueue:
    def __init__(self, results):
        self._results = list(results)
        self.added = []
        self.flushed = 0
        self.commits = 0
        self.refreshed = 0

    async def execute(self, _stmt):
        if not self._results:
            return _Result()
        return self._results.pop(0)

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        self.flushed += 1

    async def commit(self):
        self.commits += 1

    async def refresh(self, _obj):
        self.refreshed += 1


def _request(actor="tester", actor_ip="127.0.0.1", forwarded_for=None):
    headers = {"X-Actor": actor}
    if forwarded_for is not None:
        headers["X-Forwarded-For"] = forwarded_for
    return SimpleNamespace(headers=headers, client=SimpleNamespace(host=actor_ip))


def _asset(name="Sensor", entity_id="binary_sensor.teste"):
    now = datetime.now(timezone.utc)
    return Asset(
        id=uuid.uuid4(),
        asset_type="sensor",
        name=name,
        entity_id=entity_id,
        status="active",
        location="entrada",
        description=None,
        config_json=None,
        is_active=True,
        created_at=now,
        updated_at=now,
        created_by="test",
        updated_by="test",
    )


def test_asset_create_validator_rejects_empty_entity_id():
    with pytest.raises(ValidationError):
        AssetCreate(asset_type="sensor", name="X", entity_id="   ")


def test_asset_create_validator_accepts_none_config_json():
    payload = AssetCreate(asset_type="sensor", name="X", entity_id="binary_sensor.ok", config_json=None)
    assert payload.config_json is None


def test_asset_create_validator_accepts_valid_json_config():
    payload = AssetCreate(
        asset_type="sensor",
        name="X",
        entity_id="binary_sensor.ok2",
        config_json='{"topic":"ok"}',
    )
    assert payload.config_json == '{"topic":"ok"}'


def test_asset_update_validator_accepts_none_config_json():
    payload = AssetUpdate(config_json=None)
    assert payload.config_json is None


def test_asset_update_validator_rejects_invalid_json():
    with pytest.raises(ValidationError):
        AssetUpdate(config_json="{invalid-json")


def test_get_actor_ip_ignores_forwarded_chain_when_proxy_is_not_trusted():
    previous = settings.trusted_proxy_ips
    try:
        settings.trusted_proxy_ips = []
        req = _request(actor_ip="203.0.113.10", forwarded_for="192.168.1.10, 10.0.0.1")
        assert _get_actor_ip(req) == "203.0.113.10"
    finally:
        settings.trusted_proxy_ips = previous


def test_get_actor_ip_uses_forwarded_chain_when_proxy_is_trusted():
    previous = settings.trusted_proxy_ips
    try:
        settings.trusted_proxy_ips = ["203.0.113.10"]
        req = _request(actor_ip="203.0.113.10", forwarded_for="192.168.1.10, 10.0.0.1")
        assert _get_actor_ip(req) == "192.168.1.10"
    finally:
        settings.trusted_proxy_ips = previous


def test_forwarded_chain_is_normalized():
    req = _request(forwarded_for=" 192.168.1.10, invalid-ip,10.0.0.1 ")
    assert _forwarded_chain(req) == "192.168.1.10,10.0.0.1"


@pytest.mark.anyio
async def test_list_assets_executes_all_filter_paths():
    db = _DbQueue([_Result(one=1), _Result(all_rows=[])])
    result = await list_assets(
        asset_type="sensor",
        status="active",
        is_active=True,
        search="porta",
        limit=10,
        offset=2,
        db=db,
    )
    assert result["total"] == 1
    assert result["limit"] == 10
    assert result["offset"] == 2


@pytest.mark.anyio
async def test_create_asset_conflict_raises_409():
    db = _DbQueue([_Result(one_or_none=_asset())])
    payload = AssetCreate(asset_type="sensor", name="S", entity_id="binary_sensor.s")
    with pytest.raises(HTTPException) as exc:
        await create_asset(payload=payload, request=_request(), db=db)
    assert exc.value.status_code == 409


@pytest.mark.anyio
async def test_create_asset_success_creates_asset_and_audit():
    db = _DbQueue([_Result(one_or_none=None)])
    payload = AssetCreate(
        asset_type="camera",
        name="Cam Entrada",
        entity_id="camera.entrada",
        status="active",
        location="entrada",
        description="camera frontal",
        config_json='{"fps":15}',
    )
    result = await create_asset(payload=payload, request=_request(actor="admin"), db=db)

    assert result["entity_id"] == "camera.entrada"
    assert result["name"] == "Cam Entrada"
    assert db.flushed == 1
    assert db.commits == 1
    assert db.refreshed == 1
    assert len(db.added) >= 2


@pytest.mark.anyio
async def test_update_asset_not_found_raises_404():
    db = _DbQueue([_Result(one_or_none=None)])
    with pytest.raises(HTTPException) as exc:
        await update_asset(
            asset_id=uuid.uuid4(),
            payload=AssetUpdate(name="Novo"),
            request=_request(),
            db=db,
        )
    assert exc.value.status_code == 404


@pytest.mark.anyio
async def test_update_asset_success_updates_fields_and_commits():
    asset = _asset()
    db = _DbQueue([_Result(one_or_none=asset)])
    result = await update_asset(
        asset_id=asset.id,
        payload=AssetUpdate(
            name="Atualizado",
            status="maintenance",
            location="garagem",
            description="desc",
            config_json='{"k":"v"}',
            is_active=False,
        ),
        request=_request(),
        db=db,
    )
    assert result["name"] == "Atualizado"
    assert result["status"] == "maintenance"
    assert result["is_active"] is False
    assert db.commits == 1
    assert db.refreshed == 1


@pytest.mark.anyio
async def test_delete_asset_not_found_raises_404():
    db = _DbQueue([_Result(one_or_none=None)])
    with pytest.raises(HTTPException) as exc:
        await delete_asset(asset_id=uuid.uuid4(), request=_request(), db=db)
    assert exc.value.status_code == 404


@pytest.mark.anyio
async def test_restore_asset_not_found_raises_404():
    db = _DbQueue([_Result(one_or_none=None)])
    with pytest.raises(HTTPException) as exc:
        await restore_asset(asset_id=uuid.uuid4(), request=_request(), db=db)
    assert exc.value.status_code == 404


@pytest.mark.anyio
async def test_delete_asset_success_soft_deactivates_and_returns_status():
    asset = _asset()
    db = _DbQueue([_Result(one_or_none=asset)])

    result = await delete_asset(asset_id=asset.id, request=_request(actor="admin"), db=db)

    assert result["status"] == "deactivated"
    assert result["id"] == str(asset.id)
    assert asset.is_active is False
    assert asset.status == "inactive"
    assert db.commits == 1


@pytest.mark.anyio
async def test_restore_asset_success_reactivates_and_returns_asset():
    asset = _asset()
    asset.status = "inactive"
    asset.is_active = False
    db = _DbQueue([_Result(one_or_none=asset)])

    result = await restore_asset(asset_id=asset.id, request=_request(actor="admin"), db=db)

    assert result["id"] == str(asset.id)
    assert result["status"] == "active"
    assert result["is_active"] is True
    assert db.commits == 1
    assert db.refreshed == 1
