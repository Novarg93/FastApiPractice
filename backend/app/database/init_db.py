from sqlalchemy.orm.sync import update

from app.database.session import  SessionLocal
from app.models.items import Item

items_data = [
    {"name": "Orb of Transmutation", "price": 0.01, "image": "transmutation_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Orb of Alteration", "price": 0.05, "image": "alteration_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Jeweller's Orb", "price": 0.05, "image": "jewellers_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Orb of Fusing", "price": 0.1, "image": "fusing_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Orb of Scouring", "price": 0.1, "image": "scouring_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Chaos Orb", "price": 1.0, "image": "chaos_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Regal Orb", "price": 0.5, "image": "regal_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Divine Orb", "price": 50.0, "image": "divine_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Exalted Orb", "price": 40.0, "image": "exalted_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Orb of Alchemy", "price": 0.15, "image": "https://i.ibb.co/S4fvc9Zp/image.png", "quantity": 1, "quality": "0"},

    {"name": "Cartographer's Chisel", "price": 0.2, "image": "chisel.png", "quantity": 1, "quality": "0"},
    {"name": "Vaal Orb", "price": 0.3, "image": "vaal_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Fragment of the Phoenix", "price": 1.5, "image": "fragment_phoenix.png", "quantity": 1, "quality": "0"},
    {"name": "Fragment of the Chimera", "price": 1.5, "image": "fragment_chimera.png", "quantity": 1, "quality": "0"},

    {"name": "Awakener's Orb", "price": 20.0, "image": "awakener_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Orb of Unmaking", "price": 0.5, "image": "orb_unmaking.png", "quantity": 1, "quality": "0"},
    {"name": "Instability Orb", "price": 10.0, "image": "instability_orb.png", "quantity": 1, "quality": "0"},

    {"name": "Gemcutter's Prism", "price": 0.5, "image": "gcp.png", "quantity": 1, "quality": "20"},
    {"name": "Chromatic Orb", "price": 0.02, "image": "chromatic_orb.png", "quantity": 1, "quality": "0"},
    {"name": "Glassblower's Bauble", "price": 0.05, "image": "bauble.png", "quantity": 1, "quality": "0"},
]

# def fill_items():
#     db = SessionLocal()
#     for data in items_data:
#         item = Item(**data)
#         db.add(item)
#     db.commit()
#     db.close()

# def update_items():
#     db = SessionLocal()
#     item = db.query(Item).all()
#     for item in item:
#         item.image = "https://i.ibb.co/S4fvc9Zp/image.png"
#     db.commit()
#     db.close()

# def delete_all_items():
#     db = SessionLocal()
#     db.query(Item).delete()   # Удаляет все строки в таблице
#     db.commit()
#     db.close()

# if __name__ == '__main__':
#     fill_items()

# if __name__ == '__main__':
#     update_items()

# if __name__ == "__main__":
#     delete_all_items()