"""item_categories

Revision ID: e1f10fcde220
Revises: ad0450accbb9
Create Date: 2025-08-22 11:00:09.381503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1f10fcde220'
down_revision: Union[str, Sequence[str], None] = 'ad0450accbb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        sa.Table(
            "item_categories",
            sa.MetaData(),
            sa.Column("item_id", sa.Integer),
            sa.Column("category_id", sa.Integer),
        ),
        [
            # ---------------------------
            # Destiny 2 (game_id = 2, All = category_id=2)
            # ---------------------------
            {"item_id": 1, "category_id": 2}, {"item_id": 1, "category_id": 6},
            {"item_id": 2, "category_id": 2}, {"item_id": 2, "category_id": 4},
            {"item_id": 3, "category_id": 2}, {"item_id": 3, "category_id": 4},
            {"item_id": 4, "category_id": 2}, {"item_id": 4, "category_id": 4},
            {"item_id": 5, "category_id": 2}, {"item_id": 5, "category_id": 4},
            {"item_id": 6, "category_id": 2}, {"item_id": 6, "category_id": 4},
            {"item_id": 7, "category_id": 2}, {"item_id": 7, "category_id": 4},
            {"item_id": 8, "category_id": 2}, {"item_id": 8, "category_id": 4},
            {"item_id": 9, "category_id": 2}, {"item_id": 9, "category_id": 4},
            {"item_id": 10, "category_id": 2}, {"item_id": 10, "category_id": 4},
            {"item_id": 11, "category_id": 2}, {"item_id": 11, "category_id": 6},
            {"item_id": 12, "category_id": 2}, {"item_id": 12, "category_id": 6},
            {"item_id": 13, "category_id": 2}, {"item_id": 13, "category_id": 6},
            {"item_id": 14, "category_id": 2}, {"item_id": 14, "category_id": 6},
            {"item_id": 15, "category_id": 2}, {"item_id": 15, "category_id": 6},
            {"item_id": 16, "category_id": 2}, {"item_id": 16, "category_id": 6},
            {"item_id": 17, "category_id": 2}, {"item_id": 17, "category_id": 6},
            {"item_id": 18, "category_id": 2}, {"item_id": 18, "category_id": 6},
            {"item_id": 19, "category_id": 2}, {"item_id": 19, "category_id": 6},
            {"item_id": 20, "category_id": 2}, {"item_id": 20, "category_id": 6},
            {"item_id": 21, "category_id": 2}, {"item_id": 21, "category_id": 6},
            {"item_id": 22, "category_id": 2}, {"item_id": 22, "category_id": 6},

            # ---------------------------
            # Path of Exile 2 (game_id = 1, All = category_id=1)
            # ---------------------------
            {"item_id": 23, "category_id": 1}, {"item_id": 23, "category_id": 11},
            {"item_id": 24, "category_id": 1}, {"item_id": 24, "category_id": 11},
            {"item_id": 25, "category_id": 1}, {"item_id": 25, "category_id": 11},
            {"item_id": 26, "category_id": 1}, {"item_id": 26, "category_id": 11},
            {"item_id": 27, "category_id": 1}, {"item_id": 27, "category_id": 11},
            {"item_id": 28, "category_id": 1}, {"item_id": 28, "category_id": 12},
            {"item_id": 29, "category_id": 1}, {"item_id": 29, "category_id": 12},
            {"item_id": 30, "category_id": 1}, {"item_id": 30, "category_id": 12},
            {"item_id": 31, "category_id": 1}, {"item_id": 31, "category_id": 12},
            {"item_id": 32, "category_id": 1}, {"item_id": 32, "category_id": 13},
            {"item_id": 33, "category_id": 1}, {"item_id": 33, "category_id": 13},
            {"item_id": 34, "category_id": 1}, {"item_id": 34, "category_id": 13},
            {"item_id": 35, "category_id": 1}, {"item_id": 35, "category_id": 13},
            {"item_id": 36, "category_id": 1}, {"item_id": 36, "category_id": 13},
            {"item_id": 37, "category_id": 1}, {"item_id": 37, "category_id": 13},
            {"item_id": 38, "category_id": 1}, {"item_id": 38, "category_id": 13},
            {"item_id": 39, "category_id": 1}, {"item_id": 39, "category_id": 13},
            {"item_id": 40, "category_id": 1}, {"item_id": 40, "category_id": 13},

            # ---------------------------
            # Final Fantasy XIV (game_id = 3, All = category_id=3)
            # ---------------------------
            {"item_id": 41, "category_id": 3}, {"item_id": 41, "category_id": 7},
            {"item_id": 42, "category_id": 3}, {"item_id": 42, "category_id": 9},
            {"item_id": 43, "category_id": 3}, {"item_id": 43, "category_id": 8},
            {"item_id": 44, "category_id": 3}, {"item_id": 44, "category_id": 8},
            {"item_id": 45, "category_id": 3}, {"item_id": 45, "category_id": 8},
            {"item_id": 46, "category_id": 3}, {"item_id": 46, "category_id": 8},
            {"item_id": 47, "category_id": 3}, {"item_id": 47, "category_id": 8},
            {"item_id": 48, "category_id": 3}, {"item_id": 48, "category_id": 8},
            {"item_id": 49, "category_id": 3}, {"item_id": 49, "category_id": 8},
            {"item_id": 50, "category_id": 3}, {"item_id": 50, "category_id": 8},
            {"item_id": 51, "category_id": 3}, {"item_id": 51, "category_id": 8},
            {"item_id": 52, "category_id": 3}, {"item_id": 52, "category_id": 8},
            {"item_id": 53, "category_id": 3}, {"item_id": 53, "category_id": 8},
            {"item_id": 54, "category_id": 3}, {"item_id": 54, "category_id": 8},
            {"item_id": 55, "category_id": 3}, {"item_id": 55, "category_id": 8},
            {"item_id": 56, "category_id": 3}, {"item_id": 56, "category_id": 8},
            {"item_id": 57, "category_id": 3}, {"item_id": 57, "category_id": 10},
            {"item_id": 58, "category_id": 3}, {"item_id": 58, "category_id": 7},
        ]
    )


def downgrade() -> None:
    op.execute("DELETE FROM item_categories WHERE item_id BETWEEN 1 AND 58;")
