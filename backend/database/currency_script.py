from models.items import Item
from sqlalchemy.ext.asyncio import AsyncSession

items_seed_data = [
    {"name": "Chaos Orb", "description": "Standard currency for trading in Path of Exile", "price": 15, "image": ""},
    {"name": "Exalted Orb", "description": "Rare and valuable currency used for high-end crafts", "price": 180, "image": ""},
    {"name": "Divine Orb", "description": "Very valuable currency used to reroll item values", "price": 140, "image": ""},
    {"name": "Orb of Alteration", "description": "Cheap currency for basic crafting", "price": 1, "image": ""},
    {"name": "Orb of Fusing", "description": "Currency for linking sockets", "price": 6, "image": ""},
    {"name": "Orb of Alchemy", "description": "Upgrades a normal item to rare", "price": 4, "image": ""},
    {"name": "Gemcutter's Prism", "description": "Improves quality of gems", "price": 16, "image": ""},
    {"name": "Orb of Regret", "description": "Resets passive skill points", "price": 12, "image": ""},
    {"name": "Blessed Orb", "description": "Rerolls values of implicit modifiers", "price": 9, "image": ""},
    {"name": "Orb of Scouring", "description": "Removes all modifiers from an item", "price": 8, "image": ""},
    {"name": "Orb of Chance", "description": "Upgrades normal item to random rarity", "price": 2, "image": ""},
    {"name": "Cartographer's Chisel", "description": "Improves map quality", "price": 3, "image": ""},
    {"name": "Regal Orb", "description": "Upgrades a magic item to rare", "price": 10, "image": ""},
    {"name": "Vaal Orb", "description": "Corrupts an item unpredictably", "price": 15, "image": ""},
    {"name": "Chromatic Orb", "description": "Changes colors of item sockets", "price": 1, "image": ""},
    {"name": "Silver Coin", "description": "Used for prophecy content", "price": 0.5, "image": ""},
    {"name": "Perandus Coin", "description": "Currency for trading with Cadiro", "price": 0.7, "image": ""},
    {"name": "Ancient Orb", "description": "Randomizes unique item into another of same type", "price": 40, "image": ""},
    {"name": "Annulment Orb", "description": "Removes a random modifier from item", "price": 35, "image": ""},
    {"name": "Mirror of Kalandra", "description": "Extremely rare currency, duplicates item", "price": 10000, "image": ""},
]

async def seed_items(db: AsyncSession):
    for item_data in items_seed_data:
        item = Item(**item_data)
        db.add(item)
    await db.commit()
