"""Add editorial priority

Revision ID: fd71fea501a2
Revises: fa4e03c78fe6
Create Date: 2026-08-03 14:19:38.536529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd71fea501a2'
down_revision: Union[str, Sequence[str], None] = 'fa4e03c78fe6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "events",
        sa.Column(
            "editorial_priority",
            sa.String(length=20),
            nullable=False,
            server_default="Background",
        ),
    )


def downgrade() -> None:
    op.drop_column("events", "editorial_priority")
