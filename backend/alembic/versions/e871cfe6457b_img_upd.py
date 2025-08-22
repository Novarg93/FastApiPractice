"""img_upd

Revision ID: e871cfe6457b
Revises: 4b97c9a09d0a
Create Date: 2025-08-22 19:03:50.638135

"""
from typing import Sequence, Union
from sqlalchemy import text
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e871cfe6457b'
down_revision: Union[str, Sequence[str], None] = '4b97c9a09d0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Чистим путь у games
    op.execute("""
        UPDATE games
        SET image = substr(image, instr(image, 'images/'))
        WHERE image LIKE '%images/%';
    """)

    # 2. Добавляем префикс /images/ у items (если его ещё нет)
    op.execute("""
        UPDATE items
        SET image = '/images/' || image
        WHERE image NOT LIKE 'images/%';
    """)


def downgrade() -> None:
    # Откат для items (убираем префикс /images/)
    op.execute("""
        UPDATE items
        SET image = substr(image, 9)
        WHERE image LIKE '/images/%';
    """)

    # Откат для games невозможен (старые пути неизвестны),
    # поэтому оставляем как есть
    pass