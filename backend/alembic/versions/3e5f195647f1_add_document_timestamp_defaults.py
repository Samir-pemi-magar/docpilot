"""add document timestamp defaults

Revision ID: 3e5f195647f1
Revises: d60d376905ba
Create Date: 2026-09-16 17:26:50.341172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e5f195647f1'
down_revision: Union[str, Sequence[str], None] = 'd60d376905ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "documents",
        "created_at",
        server_default=sa.text("now()"),
    )

    op.alter_column(
        "documents",
        "updated_at",
        server_default=sa.text("now()"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "documents",
        "created_at",
        server_default=None,
    )

    op.alter_column(
        "documents",
        "updated_at",
        server_default=None,
    )