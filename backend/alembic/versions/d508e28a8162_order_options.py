"""order_Options

Revision ID: d508e28a8162
Revises: f5014d4f8022
Create Date: 2025-08-20 21:14:36.183208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd508e28a8162'
down_revision: Union[str, Sequence[str], None] = 'f5014d4f8022'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # таблица item_options
    op.create_table(
        "item_options",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id", ondelete="CASCADE"), nullable=False),
        sa.Column("key", sa.String(50), nullable=False),
        sa.Column("type", sa.String(20), nullable=False),  # radio, checkbox, slider...
        sa.Column("label", sa.String(100), nullable=False),
    )

    # таблица item_option_choices
    op.create_table(
        "item_option_choices",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("option_id", sa.Integer, sa.ForeignKey("item_options.id", ondelete="CASCADE"), nullable=False),
        sa.Column("value", sa.String(50), nullable=False),   # машинное значение
        sa.Column("label", sa.String(100), nullable=False),  # отображаемое
        sa.Column("pct", sa.Integer, nullable=True),         # процент
        sa.Column("abs_cents", sa.Integer, nullable=True),   # фиксированная надбавка
        sa.Column("multiplier", sa.Integer, nullable=True),  # множитель
        sa.Column("order", sa.String(20), nullable=False, server_default="pctThenAbs"),
    )


def downgrade():
    op.drop_table("item_option_choices")
    op.drop_table("item_options")