"""game update2

Revision ID: f5014d4f8022
Revises: c94e9076512c
Create Date: 2025-08-19 21:49:48.347626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5014d4f8022'
down_revision: Union[str, Sequence[str], None] = 'c94e9076512c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("""
        INSERT INTO games (id, name, slug, image, description) VALUES
        (1, 'Path of Exile 2', 'poe2', '/images/poe2.jpg', 'Currency and items'),
        (2, 'Final Fantasy XIV', 'ffxiv', '/images/ffxiv.jpg', 'MMORPG with rich lore and raids'),
        (3, 'Destiny 2', 'destiny2', '/images/d2.jpg', 'Pve and Pvp')
        ON CONFLICT(id) DO UPDATE SET
            name=excluded.name,
            slug=excluded.slug,
            image=excluded.image,
            description=excluded.description;
    """)


def downgrade():
    pass