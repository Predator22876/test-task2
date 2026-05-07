"""initial migration

Revision ID: 5cc0461fd572
Revises: 
Create Date: 2026-05-07 18:00:18.114595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cc0461fd572'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('wallets',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('balance', sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('wallets')
