"""Add homepage briefing fields

Revision ID: a1b2c3d4e5f6
Revises: f9ca905b0dee
Create Date: 2026-08-04 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "f9ca905b0dee"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "events",
        sa.Column(
            "homepage_section",
            sa.String(length=20),
            nullable=True,
        ),
    )
    op.add_column(
        "events",
        sa.Column(
            "briefing_rank",
            sa.Integer(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("events", "briefing_rank")
    op.drop_column("events", "homepage_section")
