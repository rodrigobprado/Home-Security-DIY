"""add actor_ip_chain to asset_audit

Revision ID: 20260302_0004
Revises: 20260223_0003
Create Date: 2026-03-02 00:00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20260302_0004"
down_revision: Union[str, None] = "20260223_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "asset_audit",
        sa.Column("actor_ip_chain", sa.Text(), nullable=True),
        schema="dashboard",
    )


def downgrade() -> None:
    op.drop_column("asset_audit", "actor_ip_chain", schema="dashboard")
