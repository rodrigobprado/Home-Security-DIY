import asyncio

from app.db import session as db_session


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
