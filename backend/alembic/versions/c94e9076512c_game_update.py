"""game update

Revision ID: c94e9076512c
Revises: d797a1efe64a
Create Date: 2025-08-19 21:47:15.673685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c94e9076512c'
down_revision: Union[str, Sequence[str], None] = 'd797a1efe64a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('games', sa.Column('image', sa.String(), nullable=True))
    op.add_column('games', sa.Column('description', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('games', 'description')
    op.drop_column('games', 'image')
