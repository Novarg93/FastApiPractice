"""options ugrade

Revision ID: f67768654ea7
Revises: d508e28a8162
Create Date: 2025-08-20 22:10:04.249821

"""
from typing import Sequence, Union
from sqlalchemy.orm import Session
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f67768654ea7'
down_revision: Union[str, Sequence[str], None] = 'd508e28a8162'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавляем колонки для слайдера
    with op.batch_alter_table("item_options", schema=None) as batch_op:
        batch_op.add_column(sa.Column("min_value", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("max_value", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("step", sa.Integer(), nullable=True))


def downgrade():
    # Удаляем колонки при откате
    with op.batch_alter_table("item_options", schema=None) as batch_op:
        batch_op.drop_column("step")
        batch_op.drop_column("max_value")
        batch_op.drop_column("min_value")