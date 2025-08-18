"""add items to items

Revision ID: 28da83d65df1
Revises: 3a9edb6724f0
Create Date: 2025-08-18 21:04:06.999106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28da83d65df1'
down_revision: Union[str, Sequence[str], None] = '3a9edb6724f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    items = [
        # ---------------- Path of Exile 2 (60) ----------------
        {"name": "Mirror of Kalandra", "price": 100, "image": "mirror_of_kalandra.png", "quantity": 1, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Exalted Orb", "price": 5, "image": "exalted_orb.png", "quantity": 50, "quality": "currency", "game_id": 1, "category_id": 1},
        {"name": "Chaos Orb", "price": 1, "image": "chaos_orb.png", "quantity": 200, "quality": "currency", "game_id": 1, "category_id": 1},
        {"name": "Divine Orb", "price": 15, "image": "divine_orb.png", "quantity": 30, "quality": "currency", "game_id": 1, "category_id": 1},
        {"name": "Orb of Alchemy", "price": 0.5, "image": "orb_of_alchemy.png", "quantity": 500, "quality": "currency", "game_id": 1, "category_id": 1},
        {"name": "Orb of Fusing", "price": 0.8, "image": "orb_of_fusing.png", "quantity": 300, "quality": "currency", "game_id": 1, "category_id": 1},
        {"name": "Orb of Regret", "price": 1.2, "image": "orb_of_regret.png", "quantity": 120, "quality": "currency", "game_id": 1, "category_id": 1},
        {"name": "Jeweller’s Orb", "price": 0.3, "image": "jewellers_orb.png", "quantity": 400, "quality": "currency", "game_id": 1, "category_id": 1},
        {"name": "Chromatic Orb", "price": 0.2, "image": "chromatic_orb.png", "quantity": 800, "quality": "currency", "game_id": 1, "category_id": 1},
        {"name": "Orb of Scouring", "price": 2, "image": "orb_of_scouring.png", "quantity": 80, "quality": "currency", "game_id": 1, "category_id": 1},

        {"name": "Tabula Rasa", "price": 10, "image": "tabula_rasa.png", "quantity": 10, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Kaom’s Heart", "price": 40, "image": "kaoms_heart.png", "quantity": 5, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Shavronne’s Wrappings", "price": 45, "image": "shavronnes_wrappings.png", "quantity": 3, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Headhunter", "price": 120, "image": "headhunter.png", "quantity": 1, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Mageblood", "price": 150, "image": "mageblood.png", "quantity": 1, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Atziri’s Promise", "price": 3, "image": "atziris_promise.png", "quantity": 25, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Lioneye’s Glare", "price": 7, "image": "lioneeys_glare.png", "quantity": 6, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Windripper", "price": 9, "image": "windripper.png", "quantity": 4, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Voltaxic Rift", "price": 12, "image": "voltaxic_rift.png", "quantity": 2, "quality": "unique", "game_id": 1, "category_id": 3},
        {"name": "Starforge", "price": 18, "image": "starforge.png", "quantity": 2, "quality": "unique", "game_id": 1, "category_id": 3},

        {"name": "Map: Burial Chambers", "price": 2, "image": "burial_chambers.png", "quantity": 50, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Glacier", "price": 1.5, "image": "glacier.png", "quantity": 60, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Tropical Island", "price": 1, "image": "tropical_island.png", "quantity": 70, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Dunes", "price": 1, "image": "dunes.png", "quantity": 80, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Canyon", "price": 1.2, "image": "canyon.png", "quantity": 60, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Strand", "price": 1, "image": "strand.png", "quantity": 75, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Iceberg", "price": 1.3, "image": "iceberg.png", "quantity": 40, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Underground Sea", "price": 1.5, "image": "underground_sea.png", "quantity": 30, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Jungle Valley", "price": 1.4, "image": "jungle_valley.png", "quantity": 35, "quality": "map", "game_id": 1, "category_id": 4},
        {"name": "Map: Promenade", "price": 1.2, "image": "promenade.png", "quantity": 45, "quality": "map", "game_id": 1, "category_id": 4},

        # (ещё ~30 предметов для PoE2: редкие шлемы, ботинки, оружие, аксессуары, уникальные карты, тотемы и т.д.)

        # ---------------- Final Fantasy XIV (20) ----------------
        {"name": "Ironworks Armor", "price": 20, "image": "ironworks_armor.png", "quantity": 10, "quality": "gear", "game_id": 2, "category_id": 6},
        {"name": "Allagan Tomestone", "price": 5, "image": "allagan_tomestone.png", "quantity": 100, "quality": "currency", "game_id": 2, "category_id": 7},
        {"name": "Fat Chocobo Mount", "price": 50, "image": "fat_chocobo.png", "quantity": 2, "quality": "mount", "game_id": 2, "category_id": 8},
        {"name": "Cloud’s Buster Sword", "price": 35, "image": "buster_sword.png", "quantity": 5, "quality": "weapon", "game_id": 2, "category_id": 5},
        {"name": "Ardbert’s Armor", "price": 25, "image": "ardbert_armor.png", "quantity": 3, "quality": "gear", "game_id": 2, "category_id": 6},
        {"name": "White Mage Staff", "price": 30, "image": "white_mage_staff.png", "quantity": 6, "quality": "weapon", "game_id": 2, "category_id": 5},
        {"name": "Phoenix Down", "price": 3, "image": "phoenix_down.png", "quantity": 40, "quality": "consumable", "game_id": 2, "category_id": 7},
        {"name": "Moogle Plushie", "price": 8, "image": "moogle_plushie.png", "quantity": 15, "quality": "cosmetic", "game_id": 2, "category_id": 7},
        {"name": "Black Mage Hat", "price": 15, "image": "black_mage_hat.png", "quantity": 10, "quality": "gear", "game_id": 2, "category_id": 6},
        {"name": "Dragoon Spear", "price": 22, "image": "dragoon_spear.png", "quantity": 4, "quality": "weapon", "game_id": 2, "category_id": 5},
        {"name": "Astrologian Globe", "price": 18, "image": "astrologian_globe.png", "quantity": 3, "quality": "weapon", "game_id": 2, "category_id": 5},
        {"name": "Scholar Grimoire", "price": 20, "image": "scholar_grimoire.png", "quantity": 3, "quality": "weapon", "game_id": 2, "category_id": 5},
        {"name": "Samurai Katana", "price": 26, "image": "samurai_katana.png", "quantity": 2, "quality": "weapon", "game_id": 2, "category_id": 5},
        {"name": "Summoner Book", "price": 17, "image": "summoner_book.png", "quantity": 3, "quality": "weapon", "game_id": 2, "category_id": 5},
        {"name": "Carbuncle Minion", "price": 12, "image": "carbuncle_minion.png", "quantity": 8, "quality": "pet", "game_id": 2, "category_id": 7},
        {"name": "Bahamut Figurine", "price": 28, "image": "bahamut_figurine.png", "quantity": 3, "quality": "cosmetic", "game_id": 2, "category_id": 7},
        {"name": "Gil Pouch", "price": 2, "image": "gil_pouch.png", "quantity": 500, "quality": "currency", "game_id": 2, "category_id": 7},
        {"name": "Materia Cluster", "price": 6, "image": "materia_cluster.png", "quantity": 50, "quality": "material", "game_id": 2, "category_id": 7},
        {"name": "Odin’s Armor", "price": 32, "image": "odin_armor.png", "quantity": 2, "quality": "gear", "game_id": 2, "category_id": 6},
        {"name": "Fenrir Mount", "price": 45, "image": "fenrir_mount.png", "quantity": 1, "quality": "mount", "game_id": 2, "category_id": 8},

        # ---------------- Destiny 2 (20) ----------------
        {"name": "Gjallarhorn", "price": 40, "image": "gjallarhorn.png", "quantity": 3, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "Vex Mythoclast", "price": 35, "image": "vex_mythoclast.png", "quantity": 4, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "The Last Word", "price": 30, "image": "the_last_word.png", "quantity": 6, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "Thunderlord", "price": 28, "image": "thunderlord.png", "quantity": 7, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "Ace of Spades", "price": 32, "image": "ace_of_spades.png", "quantity": 5, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "Hawkmoon", "price": 27, "image": "hawkmoon.png", "quantity": 6, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "Chaperone", "price": 29, "image": "chaperone.png", "quantity": 4, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "Trinity Ghoul", "price": 25, "image": "trinity_ghoul.png", "quantity": 5, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "Witherhoard", "price": 33, "image": "witherhoard.png", "quantity": 3, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "One Thousand Voices", "price": 37, "image": "1000_voices.png", "quantity": 2, "quality": "exotic", "game_id": 3, "category_id": 9},
        {"name": "Ascendant Shard", "price": 10, "image": "ascendant_shard.png", "quantity": 15, "quality": "material", "game_id": 3, "category_id": 12},
        {"name": "Enhancement Prism", "price": 6, "image": "enhancement_prism.png", "quantity": 25, "quality": "material", "game_id": 3, "category_id": 12},
        {"name": "Upgrade Module", "price": 3, "image": "upgrade_module.png", "quantity": 40, "quality": "material", "game_id": 3, "category_id": 12},
        {"name": "Raid Banner", "price": 2, "image": "raid_banner.png", "quantity": 50, "quality": "consumable", "game_id": 3, "category_id": 12},
        {"name": "Fallen Transmat Effect", "price": 5, "image": "fallen_transmat.png", "quantity": 20, "quality": "shader", "game_id": 3, "category_id": 11},
        {"name": "Crucible Token", "price": 4, "image": "crucible_token.png", "quantity": 70, "quality": "currency", "game_id": 3, "category_id": 12},
        {"name": "Trials Passage Coin", "price": 4, "image": "trials_passage_coin.png", "quantity": 30, "quality": "consumable", "game_id": 3, "category_id": 12},
        {"name": "Strange Coin", "price": 7, "image": "strange_coin.png", "quantity": 50, "quality": "currency", "game_id": 3, "category_id": 12},
        {"name": "Bright Engram", "price": 8, "image": "bright_engram.png", "quantity": 40, "quality": "consumable", "game_id": 3, "category_id": 12},
        {"name": "Exotic Cipher", "price": 12, "image": "exotic_cipher.png", "quantity": 10, "quality": "material", "game_id": 3, "category_id": 12},
    ]

    conn.execute(
        sa.text("""
            INSERT INTO items (name, price, image, quantity, quality, game_id, category_id)
            VALUES (:name, :price, :image, :quantity, :quality, :game_id, :category_id)
        """),
        items
    )
    conn.commit()


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM items"))
    conn.commit()