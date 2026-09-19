"""add extracted storage key to documents

Revision ID: f8c2e8371e98
Revises: c47defccc82e
Create Date: 2026-09-19 01:15:04.771712

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f8c2e8371e98"
down_revision: Union[str, Sequence[str], None] = "c47defccc82e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "documents",
        sa.Column(
            "extracted_storage_key",
            sa.String(length=500),
            nullable=True,
        ),
    )

    op.create_unique_constraint(
        "uq_documents_extracted_storage_key",
        "documents",
        ["extracted_storage_key"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uq_documents_extracted_storage_key",
        "documents",
        type_="unique",
    )

    op.drop_column(
        "documents",
        "extracted_storage_key",
    )
