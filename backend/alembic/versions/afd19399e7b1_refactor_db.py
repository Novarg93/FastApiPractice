"""refactor db

Revision ID: afd19399e7b1
Revises: 1960829b2ca6
Create Date: 2025-08-19 00:53:06.357591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afd19399e7b1'
down_revision: Union[str, Sequence[str], None] = '1960829b2ca6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('items', 'quality',
                    existingtype=sa.Integer(),
                    type=sa.String(),
                    existing_nullable=True)

def downgrade():
    op.alter_column('items', 'quality',
                    existingtype=sa.String(),
                    type=sa.Integer(),
                    existing_nullable=True)
