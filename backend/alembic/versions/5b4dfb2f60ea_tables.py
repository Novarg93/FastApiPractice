"""Tables

Revision ID: 5b4dfb2f60ea
Revises: c2ed51476344
Create Date: 2025-08-22 10:37:19.860997

"""
from typing import Sequence, Union
from sqlalchemy.dialects.postgresql import JSONB
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b4dfb2f60ea'
down_revision: Union[str, Sequence[str], None] = 'c2ed51476344'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  pass

def downgrade() -> None:
    pass