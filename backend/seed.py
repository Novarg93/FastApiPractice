from app.database.session import SessionLocal
from app.models.users import User, UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

superusers = [
    User(
        email="admin1@mail.com",
        name="Super Admin 1",
        hashed_password=pwd_context.hash("admin"),
        role=UserRole.ADMIN,
    ),
    User(
        email="support@mail.com",
        name="Support Guy",
        hashed_password=pwd_context.hash("support"),
        role=UserRole.SUPPORT,
    ),
]

for su in superusers:
    exists = db.query(User).filter(User.email == su.email).first()
    if not exists:
        db.add(su)

db.commit()
db.close()
print("✅ Superusers added")
