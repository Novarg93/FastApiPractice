"""seed in db

Revision ID: d797a1efe64a
Revises: afd19399e7b1
Create Date: 2025-08-19 20:52:34.906909

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer, String

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd797a1efe64a'
down_revision: Union[str, Sequence[str], None] = 'afd19399e7b1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    games_table = table(
        "games",
        column("id", Integer),
        column("name", String),
        column("slug", String),
    )

    categories_table = table(
        "categories",
        column("id", Integer),
        column("name", String),
        column("slug", String),
        column("game_id", Integer),
    )

    # сидим "all" категории для каждой игры
    conn = op.get_bind()

    games = conn.execute(sa.text("SELECT id, slug, name FROM games")).fetchall()

    all_cats = [
        {"id": 1000 + g.id, "name": "All", "slug": "all", "game_id": g.id}
        for g in games
    ]
    op.bulk_insert(categories_table, all_cats)

    # связываем все items с "all" своей игры
    items = conn.execute(sa.text("SELECT id, game_id FROM items")).fetchall()
    for item in items:
        # ищем id категории "all" для этой игры
        cat_id = 1000 + item.game_id
        conn.execute(
            sa.text(
                "INSERT INTO item_categories (item_id, category_id) VALUES (:i, :c)"
            ),
            {"i": item.id, "c": cat_id},
        )

    # также можно засидить конкретные связи item -> category, если знаешь правила
    # пример: все предметы с quality='currency' в category 'currency'
    # conn.execute("INSERT ... ")


def downgrade() -> None:
    conn = op.get_bind()
    # чистим связи
    conn.execute(sa.text("DELETE FROM item_categories WHERE category_id >= 1000"))
    # чистим all категории
    conn.execute(sa.text("DELETE FROM categories WHERE slug='all'"))
