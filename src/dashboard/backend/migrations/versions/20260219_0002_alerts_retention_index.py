"""add alerts severity-timestamp index

Revision ID: 20260219_0002
Revises: 20260219_0001
Create Date: 2026-02-19 00:20:00
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260219_0002"
down_revision: Union[str, None] = "20260219_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(
        "ix_dashboard_alerts_severity_timestamp",
        "alerts",
        ["severity", "timestamp"],
        unique=False,
        schema="dashboard",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_dashboard_alerts_severity_timestamp",
        table_name="alerts",
        schema="dashboard",
    )
