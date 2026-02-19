"""initial dashboard schema

Revision ID: 20260219_0001
Revises:
Create Date: 2026-02-19 00:00:01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "20260219_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS dashboard")

    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("entity_id", sa.String(length=200), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("old_state", sa.String(length=200), nullable=True),
        sa.Column("new_state", sa.String(length=200), nullable=True),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_alerts_entity_id",
        "alerts",
        ["entity_id"],
        unique=False,
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_alerts_timestamp",
        "alerts",
        ["timestamp"],
        unique=False,
        schema="dashboard",
    )

    op.create_table(
        "dashboard_config",
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("value", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("key"),
        schema="dashboard",
    )

    op.create_table(
        "device_positions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("entity_id", sa.String(length=200), nullable=False),
        sa.Column("label", sa.String(length=100), nullable=False),
        sa.Column("x", sa.Float(), nullable=False),
        sa.Column("y", sa.Float(), nullable=False),
        sa.Column("device_type", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("entity_id"),
        schema="dashboard",
    )


def downgrade() -> None:
    op.drop_table("device_positions", schema="dashboard")
    op.drop_table("dashboard_config", schema="dashboard")
    op.drop_index("ix_dashboard_alerts_timestamp", table_name="alerts", schema="dashboard")
    op.drop_index("ix_dashboard_alerts_entity_id", table_name="alerts", schema="dashboard")
    op.drop_table("alerts", schema="dashboard")
