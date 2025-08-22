"""Seed

Revision ID: ad0450accbb9
Revises: 5b4dfb2f60ea
Create Date: 2025-08-22 10:41:54.929626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad0450accbb9'
down_revision: Union[str, Sequence[str], None] = '5b4dfb2f60ea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Заполнение таблицы 'games' ---
    op.bulk_insert(
        sa.Table(
            'games',
            sa.MetaData(),
            sa.Column('id', sa.Integer),
            sa.Column('name', sa.String),
            sa.Column('slug', sa.String),
            sa.Column('image', sa.String),
            sa.Column('description', sa.String),
        ),
        [
            {'id': 1, 'name': 'Path of Exile 2', 'slug': 'poe2', 'image': 'poe2/images/poe2.jpg', 'description': 'Currency and items'},
            {'id': 2, 'name': 'Destiny 2', 'slug': 'd2', 'image': 'd2/images/d2.jpg', 'description': 'Pve and Pvp'},
            {'id': 3, 'name': 'Final Fantasy XIV', 'slug': 'ffxiv', 'image': 'ffxiv/images/ffxiv.jpg', 'description': 'MMORPG with rich lore and raids'},
            {'id': 4, 'name': 'Diablo 4', 'slug': 'd4', 'image': 'd4/images/d4.png', 'description': 'Gold and best gear;'},
        ]
    )

    # --- Заполнение таблицы 'categories' ---
    op.bulk_insert(
        sa.Table(
            'categories',
            sa.MetaData(),
            sa.Column('id', sa.Integer),
            sa.Column('name', sa.String),
            sa.Column('slug', sa.String),
            sa.Column('game_id', sa.Integer),
        ),
        [
            {'id': 1, 'name': 'All', 'slug': 'all', 'game_id': 1},
            {'id': 2, 'name': 'All', 'slug': 'all', 'game_id': 2},
            {'id': 3, 'name': 'All', 'slug': 'all', 'game_id': 3},
            {'id': 4, 'name': 'General', 'slug': 'general', 'game_id': 2},
            {'id': 5, 'name': 'Shader', 'slug': 'shader', 'game_id': 2},
            {'id': 6, 'name': 'Exotic', 'slug': 'exotic', 'game_id': 2},
            {'id': 7, 'name': 'Mount', 'slug': 'mount', 'game_id': 3},
            {'id': 8, 'name': 'General', 'slug': 'general', 'game_id': 3},
            {'id': 9, 'name': 'Gear', 'slug': 'gear', 'game_id': 3},
            {'id': 10, 'name': 'Weapon', 'slug': 'weapon', 'game_id': 3},
            {'id': 11, 'name': 'Map', 'slug': 'map', 'game_id': 1},
            {'id': 12, 'name': 'Unique', 'slug': 'unique', 'game_id': 1},
            {'id': 13, 'name': 'Currency', 'slug': 'currency', 'game_id': 1},
        ]
    )

    # --- Заполнение таблицы 'items' ---
    op.bulk_insert(
        sa.Table(
            'items',
            sa.MetaData(),
            sa.Column('id', sa.Integer),
            sa.Column('name', sa.String),
            sa.Column('price', sa.Float),
            sa.Column('image', sa.String),
            sa.Column('quantity', sa.Integer),
            sa.Column('quality', sa.String),
            sa.Column('game_id', sa.Integer),
        ),
        [
            # Destiny 2 (id 1–22)
            {'id': 1, 'name': 'Exotic Cipher', 'price': 15, 'image': 'exotic_cipher.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 2, 'name': 'Bright Engram', 'price': 10, 'image': 'bright_engram.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 3, 'name': 'Strange Coin', 'price': 5, 'image': 'strange_coin.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 4, 'name': 'Raid Token', 'price': 20, 'image': 'raid_token.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 5, 'name': 'Legendary Shard', 'price': 25, 'image': 'legendary_shard.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 6, 'name': 'Ascendant Shard', 'price': 40, 'image': 'ascendant_shard.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 7, 'name': 'Enhancement Core', 'price': 12, 'image': 'enhancement_core.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 8, 'name': 'Upgrade Module', 'price': 8, 'image': 'upgrade_module.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 9, 'name': 'Glimmer', 'price': 3, 'image': 'glimmer.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 10, 'name': 'Silver', 'price': 100, 'image': 'silver.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 11, 'name': 'One Thousand Voices', 'price': 140, 'image': '1000_voices.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 12, 'name': 'Anarchy', 'price': 120, 'image': 'anarchy.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 13, 'name': 'The Lament', 'price': 90, 'image': 'the_lament.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 14, 'name': 'Divinity', 'price': 150, 'image': 'divinity.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 15, 'name': "Izanagi's Burden", 'price': 110, 'image': 'izanagis_burden.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 16, 'name': 'Whisper of the Worm', 'price': 95, 'image': 'whisper_of_the_worm.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 17, 'name': 'Sleeper Simulant', 'price': 85, 'image': 'sleeper_simulant.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 18, 'name': 'Thunderlord', 'price': 70, 'image': 'thunderlord.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 19, 'name': 'Xenophage', 'price': 100, 'image': 'xenophage.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 20, 'name': 'Gjallarhorn', 'price': 160, 'image': 'gjallarhorn.png', 'quantity': 1, 'quality': '1',
             'game_id': 2},
            {'id': 21, 'name': 'Vex Mythoclast', 'price': 130, 'image': 'vex_mythoclast.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},
            {'id': 22, 'name': 'Eyes of Tomorrow', 'price': 125, 'image': 'eyes_of_tomorrow.png', 'quantity': 1,
             'quality': '1', 'game_id': 2},

            # Path of Exile 2 (id 23–40)
            {'id': 23, 'name': 'Map: Canyon', 'price': 15, 'image': 'canyon.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 24, 'name': 'Map: Dunes', 'price': 15, 'image': 'dunes.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 25, 'name': 'Map: Tropical Island', 'price': 20, 'image': 'tropical_island.png', 'quantity': 1,
             'quality': '1', 'game_id': 1},
            {'id': 26, 'name': 'Map: Glacier', 'price': 20, 'image': 'glacier.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 27, 'name': 'Map: Beach', 'price': 10, 'image': 'beach.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 28, 'name': 'Starforge', 'price': 150, 'image': 'starforge.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 29, 'name': 'Headhunter', 'price': 200, 'image': 'headhunter.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 30, 'name': 'Mageblood', 'price': 250, 'image': 'mageblood.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 31, 'name': 'Mirror of Kalandra', 'price': 300, 'image': 'mirror_of_kalandra.png', 'quantity': 1,
             'quality': '1', 'game_id': 1},
            {'id': 32, 'name': 'Exalted Orb', 'price': 50, 'image': 'exalted_orb.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 33, 'name': 'Divine Orb', 'price': 60, 'image': 'divine_orb.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 34, 'name': 'Chaos Orb', 'price': 5, 'image': 'chaos_orb.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 35, 'name': 'Orb of Regret', 'price': 8, 'image': 'orb_of_regret.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 36, 'name': 'Orb of Fusing', 'price': 6, 'image': 'orb_of_fusing.png', 'quantity': 1, 'quality': '1',
             'game_id': 1},
            {'id': 37, 'name': 'Orb of Alchemy', 'price': 7, 'image': 'orb_of_alchemy.png', 'quantity': 1,
             'quality': '1', 'game_id': 1},
            {'id': 38, 'name': "Gemcutter's Prism", 'price': 10, 'image': 'gemcutters_prism.png', 'quantity': 1,
             'quality': '1', 'game_id': 1},
            {'id': 39, 'name': "Awakener's Orb", 'price': 45, 'image': 'awakeners_orb.png', 'quantity': 1,
             'quality': '1', 'game_id': 1},
            {'id': 40, 'name': 'Orb of Annulment', 'price': 20, 'image': 'orb_of_annulment.png', 'quantity': 1,
             'quality': '1', 'game_id': 1},

            # Final Fantasy XIV (id 41–58)
            {'id': 41, 'name': 'Fenrir Mount', 'price': 120, 'image': 'fenrir_mount.png', 'quantity': 1, 'quality': '1',
             'game_id': 3},
            {'id': 42, 'name': 'Odin’s Armor', 'price': 140, 'image': 'odin_armor.png', 'quantity': 1, 'quality': '1',
             'game_id': 3},
            {'id': 43, 'name': 'Materia Cluster', 'price': 35, 'image': 'materia_cluster.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 44, 'name': 'Gil', 'price': 3, 'image': 'gil.png', 'quantity': 1, 'quality': '1', 'game_id': 3},
            {'id': 45, 'name': 'Allagan Tomestone', 'price': 25, 'image': 'allagan_tomestone.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 46, 'name': 'Extreme Trial Boost', 'price': 60, 'image': 'extreme_trial_boost.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 47, 'name': 'Savage Raid Boost', 'price': 90, 'image': 'savage_raid_boost.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 48, 'name': 'Ultimate Raid Boost', 'price': 150, 'image': 'ultimate_raid_boost.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 49, 'name': 'Deep Dungeon Boost', 'price': 55, 'image': 'deep_dungeon_boost.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 50, 'name': 'Leveling Boost', 'price': 40, 'image': 'leveling_boost.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 51, 'name': 'Glamour Prism', 'price': 5, 'image': 'glamour_prism.png', 'quantity': 1, 'quality': '1',
             'game_id': 3},
            {'id': 52, 'name': 'Housing Item', 'price': 15, 'image': 'housing_item.png', 'quantity': 1, 'quality': '1',
             'game_id': 3},
            {'id': 53, 'name': 'Crafting Material', 'price': 10, 'image': 'crafting_material.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 54, 'name': 'Gathering Material', 'price': 10, 'image': 'gathering_material.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 55, 'name': 'Minion', 'price': 20, 'image': 'minion.png', 'quantity': 1, 'quality': '1',
             'game_id': 3},
            {'id': 56, 'name': 'Orchestrion Roll', 'price': 8, 'image': 'orchestrion_roll.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 57, 'name': "Cloud’s Buster Sword", 'price': 180, 'image': 'buster_sword.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
            {'id': 58, 'name': 'Fat Chocobo Mount', 'price': 100, 'image': 'fat_chocobo.png', 'quantity': 1,
             'quality': '1', 'game_id': 3},
        ]
    )

    # --- Заполнение таблицы 'options' ---
    op.bulk_insert(
        sa.Table(
            'options',
            sa.MetaData(),
            sa.Column('id', sa.Integer),
            sa.Column('name', sa.String), # Изменен с 'key' на 'name'
            sa.Column('label', sa.String),
            sa.Column('type', sa.String), # Изменен на String, так как Enum('radio', 'slider', 'select')
            sa.Column('min_value', sa.Integer), # Изменен с 'min' на 'min_value'
            sa.Column('max_value', sa.Integer), # Изменен с 'max' на 'max_value'
            sa.Column('step', sa.Integer),
        ),
        [
            {'id': 1, 'name': 'method', 'label': 'Метод игры', 'type': 'radio', 'min_value': None, 'max_value': None, 'step': None},
            {'id': 2, 'name': 'speed', 'label': 'Скорость', 'type': 'radio', 'min_value': None, 'max_value': None, 'step': None},
            {'id': 3, 'name': 'quantity', 'label': 'Количество', 'type': 'slider', 'min_value': 1, 'max_value': 10, 'step': 1},
        ]
    )

    # --- Заполнение таблицы 'option_choices' ---
    op.bulk_insert(
        sa.Table(
            'option_choices',
            sa.MetaData(),
            sa.Column('id', sa.Integer),
            sa.Column('option_id', sa.Integer),
            sa.Column('value', sa.String),
            sa.Column('label', sa.String),
            sa.Column('pct', sa.Float),
            sa.Column('abs_cents', sa.Integer),
            sa.Column('multiplier', sa.Float),
            sa.Column('sort_order', sa.Integer), # Добавлено поле sort_order
        ),
        [
            {'id': 1, 'option_id': 1, 'value': 'pilot', 'label': 'Пилот', 'pct': 0.0, 'abs_cents': 0, 'multiplier': 1.0, 'sort_order': 0},
            {'id': 2, 'option_id': 1, 'value': 'selfplay', 'label': 'В пати', 'pct': 0.2, 'abs_cents': 0, 'multiplier': 1.0, 'sort_order': 0},
            {'id': 3, 'option_id': 2, 'value': 'normal', 'label': 'Обычный', 'pct': 0.0, 'abs_cents': 0, 'multiplier': 1.0, 'sort_order': 0},
            {'id': 4, 'option_id': 2, 'value': 'express', 'label': 'Экспресс', 'pct': 0.2, 'abs_cents': 0, 'multiplier': 1.0, 'sort_order': 0},
        ]
    )

    # --- Заполнение таблицы 'product_options' ---
    # В модели Option ProductOption ссылается на products.id, а не items.id.
    # Если ProductOption фактически является ItemOption, то product_id должно быть item_id.
    # Сейчас я использую 'product_id', как указано в вашей модели ProductOption.
    # Предполагаем, что у вас есть Product с id=32 (аналогично item_id=32)

def downgrade() -> None:
    # Удаляем данные в обратном порядке
    op.execute(sa.text("DELETE FROM product_options WHERE product_id IN (1, 32, 41) AND option_id IN (1, 2, 3)"))
    op.execute(sa.text("DELETE FROM option_choices WHERE id IN (1, 2, 3, 4)"))
    op.execute(sa.text("DELETE FROM options WHERE id IN (1, 2, 3)"))
    op.execute(sa.text("DELETE FROM items WHERE id BETWEEN 1 AND 58"))
    op.execute(sa.text("DELETE FROM categories WHERE id BETWEEN 1 AND 13"))
    op.execute(sa.text("DELETE FROM games WHERE id BETWEEN 1 AND 4"))