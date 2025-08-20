"""options seed upgrade

Revision ID: 51b5597331b3
Revises: f67768654ea7
Create Date: 2025-08-20 22:26:48.976120

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import select
from typing import Union, Sequence


# revision identifiers, used by Alembic.
revision: str = '51b5597331b3'
down_revision: Union[str, Sequence[str], None] = 'f67768654ea7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    # Таблицы
    items = sa.Table(
        "items",
        sa.MetaData(),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("quality", sa.String),
    )

    item_options = sa.Table(
        "item_options",
        sa.MetaData(),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("item_id", sa.Integer, sa.ForeignKey("items.id")),
        sa.Column("key", sa.String),
        sa.Column("type", sa.String),
        sa.Column("label", sa.String),
        sa.Column("min_value", sa.Integer),
        sa.Column("max_value", sa.Integer),
        sa.Column("step", sa.Integer),
    )

    item_option_choices = sa.Table(
        "item_option_choices",
        sa.MetaData(),
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("option_id", sa.Integer, sa.ForeignKey("item_options.id")),
        sa.Column("value", sa.String),
        sa.Column("label", sa.String),
        sa.Column("pct", sa.Float),
        sa.Column("abs_cents", sa.Integer),
        sa.Column("multiplier", sa.Float),
        sa.Column("order", sa.Integer),
    )

    # ========================
    # Currency items → slider + radio
    # ========================
    currency_items = conn.execute(
        select(items.c.id).where(items.c.quality == "currency")
    ).fetchall()

    for row in currency_items:
        # Slider "Quantity"
        conn.execute(
            item_options.insert().values(
                item_id=row.id,
                key="quantity",
                type="slider",
                label="Quantity",
                min_value=10,
                max_value=1000,
                step=10,
            )
        )

        # Radio "Delivery"
        res = conn.execute(
            item_options.insert().values(
                item_id=row.id,
                key="delivery",
                type="radio",
                label="Delivery",
            )
        )
        option_id = res.inserted_primary_key[0]

        delivery_choices = [
            {"value": "normal", "label": "Normal", "pct": 0, "abs_cents": 0, "multiplier": 1.0, "order": 1},
            {"value": "express", "label": "Express", "pct": 20, "abs_cents": 0, "multiplier": 1.2, "order": 2},
        ]

        for c in delivery_choices:
            conn.execute(item_option_choices.insert().values(option_id=option_id, **c))

    # ========================
    # Non-currency items → radio
    # ========================
    non_currency_items = conn.execute(
        select(items.c.id).where(items.c.quality != "currency")
    ).fetchall()

    for row in non_currency_items:
        res = conn.execute(
            item_options.insert().values(
                item_id=row.id,
                key="method",
                type="radio",
                label="Method",
            )
        )
        option_id = res.inserted_primary_key[0]

        method_choices = [
            {"value": "pilot", "label": "Pilot", "pct": 0, "abs_cents": 0, "multiplier": 1.0, "order": 1},
            {"value": "selfplay", "label": "Self-play", "pct": 0, "abs_cents": 0, "multiplier": 1.0, "order": 2},
            {"value": "normal", "label": "Normal", "pct": 0, "abs_cents": 0, "multiplier": 1.0, "order": 3},
            {"value": "express", "label": "Express", "pct": 20, "abs_cents": 0, "multiplier": 1.2, "order": 4},
        ]

        for c in method_choices:
            conn.execute(item_option_choices.insert().values(option_id=option_id, **c))

from sqlalchemy import text
# ...
def downgrade():
    conn = op.get_bind()
    conn.execute(text("DELETE FROM item_option_choices"))
    conn.execute(text("DELETE FROM item_options"))