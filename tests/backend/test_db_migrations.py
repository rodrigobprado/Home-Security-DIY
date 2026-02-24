import asyncio
import importlib.util
import os
import uuid

from app.db import session as db_session
from app.db.models import Asset, AssetAudit, AssetCredential


class _FakeConfig:
    def __init__(self, path):
        self.path = path
        self.options = {}

    def set_main_option(self, key, value):
        self.options[key] = value


def test_init_db_uses_alembic_upgrade_head(monkeypatch):
    calls = {}

    monkeypatch.setattr(db_session, "Config", _FakeConfig)

    def _fake_upgrade(cfg, revision):
        calls["config"] = cfg
        calls["revision"] = revision

    async def _fake_to_thread(fn):
        fn()

    monkeypatch.setattr(db_session.command, "upgrade", _fake_upgrade)
    monkeypatch.setattr(db_session.asyncio, "to_thread", _fake_to_thread)

    asyncio.run(db_session.init_db())

    assert calls["revision"] == "head"
    assert calls["config"].options["script_location"].endswith("migrations")
    assert calls["config"].options["sqlalchemy.url"].startswith("postgresql+psycopg://")


# ---------------------------------------------------------------------------
# Testes de modelos — Issue #335
# ---------------------------------------------------------------------------


class TestAssetModel:
    """Valida estrutura e defaults do modelo Asset."""

    def test_asset_model_has_required_fields(self):
        asset = Asset(
            id=uuid.uuid4(),
            asset_type="sensor",
            name="Sensor Porta",
            entity_id="binary_sensor.porta_entrada",
            status="active",
            is_active=True,
        )
        assert asset.asset_type == "sensor"
        assert asset.name == "Sensor Porta"
        assert asset.entity_id == "binary_sensor.porta_entrada"
        assert asset.status == "active"
        assert asset.is_active is True

    def test_asset_types_accepted(self):
        for asset_type in ("sensor", "camera", "ugv", "uav"):
            asset = Asset(
                id=uuid.uuid4(),
                asset_type=asset_type,
                name=f"Ativo {asset_type}",
                entity_id=f"test.{asset_type}_{uuid.uuid4().hex[:6]}",
                status="active",
                is_active=True,
            )
            assert asset.asset_type == asset_type

    def test_asset_status_accepted(self):
        for status in ("active", "inactive", "offline", "maintenance"):
            asset = Asset(
                id=uuid.uuid4(),
                asset_type="sensor",
                name="Teste",
                entity_id=f"test.sensor_{uuid.uuid4().hex[:6]}",
                status=status,
                is_active=True,
            )
            assert asset.status == status

    def test_asset_id_is_uuid(self):
        asset_id = uuid.uuid4()
        asset = Asset(
            id=asset_id,
            asset_type="camera",
            name="Camera Entrada",
            entity_id="camera.entrada",
            status="active",
            is_active=True,
        )
        assert asset.id == asset_id
        assert isinstance(asset.id, uuid.UUID)

    def test_asset_optional_fields_accept_none(self):
        asset = Asset(
            id=uuid.uuid4(),
            asset_type="sensor",
            name="Sensor",
            entity_id="binary_sensor.test",
            status="active",
            is_active=True,
            location=None,
            description=None,
            config_json=None,
            created_by=None,
            updated_by=None,
        )
        assert asset.location is None
        assert asset.description is None
        assert asset.config_json is None


class TestAssetCredentialModel:
    """Valida estrutura do modelo AssetCredential."""

    def test_credential_stores_reference_not_secret(self):
        asset_id = uuid.uuid4()
        cred = AssetCredential(
            asset_id=asset_id,
            credential_ref="vault://cameras/cam_entrada/rtsp_password",
        )
        assert cred.asset_id == asset_id
        assert cred.credential_ref.startswith("vault://")
        assert cred.last_rotated_at is None

    def test_credential_ref_is_not_plain_password(self):
        cred = AssetCredential(
            asset_id=uuid.uuid4(),
            credential_ref="k8s://secret/cam-credentials/rtsp_url",
        )
        assert "://" in cred.credential_ref  # deve ser uma referência com scheme


class TestAssetAuditModel:
    """Valida estrutura e variantes de ação do modelo AssetAudit."""

    def test_audit_create(self):
        audit = AssetAudit(
            asset_id=uuid.uuid4(),
            action="create",
            after_json='{"name":"Sensor","asset_type":"sensor"}',
            actor="admin",
            actor_ip="192.168.1.100",
        )
        assert audit.action == "create"
        assert audit.before_json is None

    def test_audit_update(self):
        audit = AssetAudit(
            asset_id=uuid.uuid4(),
            action="update",
            before_json='{"status":"active"}',
            after_json='{"status":"inactive"}',
            actor="operator",
        )
        assert audit.action == "update"
        assert audit.before_json is not None
        assert audit.after_json is not None

    def test_audit_delete(self):
        audit = AssetAudit(
            asset_id=uuid.uuid4(),
            action="delete",
            before_json='{"name":"Sensor Removido","asset_type":"sensor"}',
            actor="admin",
        )
        assert audit.action == "delete"
        assert audit.after_json is None

    def test_audit_restore(self):
        audit = AssetAudit(
            asset_id=uuid.uuid4(),
            action="restore",
            after_json='{"is_active":true}',
            actor="admin",
        )
        assert audit.action == "restore"

    def test_audit_asset_id_nullable(self):
        audit = AssetAudit(
            asset_id=None,
            action="delete",
            before_json='{"entity_id":"sensor.deletado_permanentemente"}',
            actor="system",
        )
        assert audit.asset_id is None


class TestMigration0003:
    """Valida integridade do arquivo de migração 0003."""

    def _load_migration(self):
        base = os.path.dirname(__file__)
        path = os.path.join(
            base,
            "../../src/dashboard/backend/migrations/versions",
            "20260223_0003_assets_catalog_and_audit.py",
        )
        spec = importlib.util.spec_from_file_location("migration_0003", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_migration_file_exists(self):
        base = os.path.dirname(__file__)
        path = os.path.join(
            base,
            "../../src/dashboard/backend/migrations/versions",
            "20260223_0003_assets_catalog_and_audit.py",
        )
        assert os.path.isfile(path), f"Migração 0003 não encontrada em {path}"

    def test_migration_revision(self):
        mod = self._load_migration()
        assert mod.revision == "20260223_0003"
        assert mod.down_revision == "20260219_0002"

    def test_migration_has_upgrade_and_downgrade(self):
        mod = self._load_migration()
        assert callable(mod.upgrade)
        assert callable(mod.downgrade)
