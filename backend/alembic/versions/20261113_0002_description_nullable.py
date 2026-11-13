"""make items.description nullable

Revision ID: 20261113_0002
Revises: 20261017_0001
Create Date: 2026-11-13
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "20261113_0002"
down_revision: str | None = "20261017_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("items", "description", existing_type=sa.Text(), nullable=True)


def downgrade() -> None:
    op.execute("UPDATE items SET description = '' WHERE description IS NULL")
    op.alter_column("items", "description", existing_type=sa.Text(), nullable=False)
