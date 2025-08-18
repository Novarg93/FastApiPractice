"""add avatar to users

Revision ID: 6e48b5f1a25c
Revises: 5fe17c7cb790
Create Date: 2025-08-13 22:10:07.071306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e48b5f1a25c'
down_revision: Union[str, Sequence[str], None] = '5fe17c7cb790'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('users') as b:
        b.add_column(sa.Column('avatar_url', sa.String(512), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('users') as b:
        b.drop_column('avatar_url')
