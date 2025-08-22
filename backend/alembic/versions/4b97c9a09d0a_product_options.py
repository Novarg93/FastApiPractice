"""product_options

Revision ID: 4b97c9a09d0a
Revises: e1f10fcde220
Create Date: 2025-08-22 11:05:48.579491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b97c9a09d0a'
down_revision: Union[str, Sequence[str], None] = 'e1f10fcde220'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # все товары будут иметь method (1) и speed (2)
    base_pairs = []
    for item_id in range(1, 59):
        base_pairs.append({"product_id": item_id, "option_id": 1})
        base_pairs.append({"product_id": item_id, "option_id": 2})

    # товары категории Currency (PoE2, id 32–40) получают ещё и quantity (3)
    for item_id in range(32, 41):
        base_pairs.append({"product_id": item_id, "option_id": 3})

    op.bulk_insert(
        sa.Table(
            "product_options",
            sa.MetaData(),
            sa.Column("product_id", sa.Integer),
            sa.Column("option_id", sa.Integer),
        ),
        base_pairs,
    )


def downgrade() -> None:
    op.execute("DELETE FROM product_options WHERE product_id BETWEEN 1 AND 58;")
