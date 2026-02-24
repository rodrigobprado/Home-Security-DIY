"""add assets catalog, credentials and audit trail

Revision ID: 20260223_0003
Revises: 20260219_0002
Create Date: 2026-02-23 00:00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260223_0003"
down_revision: Union[str, None] = "20260219_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- tabela principal de ativos ---
    op.create_table(
        "assets",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("asset_type", sa.String(length=20), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("entity_id", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("config_json", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("updated_by", sa.String(length=100), nullable=True),
        sa.CheckConstraint(
            "asset_type IN ('sensor', 'camera', 'ugv', 'uav')",
            name="ck_assets_asset_type",
        ),
        sa.CheckConstraint(
            "status IN ('active', 'inactive', 'offline', 'maintenance')",
            name="ck_assets_status",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("entity_id"),
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_assets_asset_type",
        "assets",
        ["asset_type"],
        unique=False,
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_assets_is_active",
        "assets",
        ["is_active"],
        unique=False,
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_assets_updated_at",
        "assets",
        ["updated_at"],
        unique=False,
        schema="dashboard",
    )

    # --- tabela de credenciais (apenas referências, sem valores reais) ---
    op.create_table(
        "asset_credentials",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("credential_ref", sa.String(length=500), nullable=False),
        sa.Column("last_rotated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["dashboard.assets.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_asset_credentials_asset_id",
        "asset_credentials",
        ["asset_id"],
        unique=False,
        schema="dashboard",
    )

    # --- trilha de auditoria ---
    op.create_table(
        "asset_audit",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("asset_id", sa.Uuid(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(length=20), nullable=False),
        sa.Column("before_json", sa.Text(), nullable=True),
        sa.Column("after_json", sa.Text(), nullable=True),
        sa.Column("actor", sa.String(length=100), nullable=True),
        sa.Column("actor_ip", sa.String(length=45), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "action IN ('create', 'update', 'delete', 'restore')",
            name="ck_asset_audit_action",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_asset_audit_asset_id",
        "asset_audit",
        ["asset_id"],
        unique=False,
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_asset_audit_created_at",
        "asset_audit",
        ["created_at"],
        unique=False,
        schema="dashboard",
    )
    op.create_index(
        "ix_dashboard_asset_audit_actor",
        "asset_audit",
        ["actor"],
        unique=False,
        schema="dashboard",
    )

    # --- backfill: migrar device_positions -> assets ---
    op.execute(
        """
        INSERT INTO dashboard.assets (id, asset_type, name, entity_id, status, location,
                                      is_active, created_at, updated_at, created_by)
        SELECT
            gen_random_uuid(),
            CASE device_type
                WHEN 'camera' THEN 'camera'
                WHEN 'drone'  THEN 'ugv'
                ELSE 'sensor'
            END,
            label,
            entity_id,
            'active',
            NULL,
            true,
            now(),
            now(),
            'migration_backfill'
        FROM dashboard.device_positions
        ON CONFLICT (entity_id) DO NOTHING
        """
    )


def downgrade() -> None:
    op.drop_index(
        "ix_dashboard_asset_audit_actor",
        table_name="asset_audit",
        schema="dashboard",
    )
    op.drop_index(
        "ix_dashboard_asset_audit_created_at",
        table_name="asset_audit",
        schema="dashboard",
    )
    op.drop_index(
        "ix_dashboard_asset_audit_asset_id",
        table_name="asset_audit",
        schema="dashboard",
    )
    op.drop_table("asset_audit", schema="dashboard")

    op.drop_index(
        "ix_dashboard_asset_credentials_asset_id",
        table_name="asset_credentials",
        schema="dashboard",
    )
    op.drop_table("asset_credentials", schema="dashboard")

    op.drop_index(
        "ix_dashboard_assets_updated_at",
        table_name="assets",
        schema="dashboard",
    )
    op.drop_index(
        "ix_dashboard_assets_is_active",
        table_name="assets",
        schema="dashboard",
    )
    op.drop_index(
        "ix_dashboard_assets_asset_type",
        table_name="assets",
        schema="dashboard",
    )
    op.drop_table("assets", schema="dashboard")
