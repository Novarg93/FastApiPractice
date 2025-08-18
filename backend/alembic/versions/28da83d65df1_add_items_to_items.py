"""add items to items

Revision ID: 28da83d65df1
Revises: 3a9edb6724f0
Create Date: 2025-08-18 21:04:06.999106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28da83d65df1'
down_revision: Union[str, Sequence[str], None] = '3a9edb6724f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass