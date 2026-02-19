#!/usr/bin/env python3
"""Cleanup old dashboard alerts based on retention policy."""

from __future__ import annotations

import asyncio
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Ensure backend modules are importable when script runs from repository root.
BACKEND_DIR = Path(__file__).resolve().parents[1] / "src" / "dashboard" / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from app.config import settings
from app.db.models import Alert


def _database_url() -> str:
    return os.getenv("DATABASE_URL", settings.database_url)


def _retention_days() -> int:
    raw = os.getenv("ALERT_RETENTION_DAYS", str(settings.alert_retention_days))
    return max(int(raw), 1)


async def _run() -> None:
    retention_days = _retention_days()
    cutoff = datetime.now(timezone.utc) - timedelta(days=retention_days)
    engine = create_async_engine(_database_url(), echo=False, pool_pre_ping=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        result = await session.execute(
            delete(Alert).where(Alert.timestamp < cutoff)
        )
        await session.commit()
        deleted = int(result.rowcount or 0)

    await engine.dispose()
    print(
        f"[cleanup_alerts] retention_days={retention_days} cutoff={cutoff.isoformat()} deleted={deleted}"
    )


if __name__ == "__main__":
    asyncio.run(_run())
