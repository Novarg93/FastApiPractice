from datetime import datetime
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models import User
from app.models.chat import ChatRoom, ChatParticipant
from app.models.orders import Order

def run_seed():
    db: Session = SessionLocal()

    # 1. Добавляем тестового юзера
    user = db.query(User).filter_by(id=1).first()
    if not user:
        user = User(
            id=1,
            name="Test User",
            email="test@mail.com",
            hashed_password="not_hashed_123",  # ⚠️ для тестов можно просто строку
            avatar_url=None
        )
        db.add(user)

    # 2. Добавляем заказ
    order = db.query(Order).filter_by(id=1).first()
    if not order:
        order = Order(
            id=1,
            user_id=1,
            status="open",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(order)

    # 3. Добавляем чат
    chat = db.query(ChatRoom).filter_by(id=1).first()
    if not chat:
        chat = ChatRoom(
            id=1,
            order_id=1,
            created_at=datetime.utcnow()
        )
        db.add(chat)

    # 4. Добавляем участника чата
    participant = db.query(ChatParticipant).filter_by(chat_id=1, user_id=1).first()
    if not participant:
        participant = ChatParticipant(
            chat_id=1,
            user_id=1,
            role_in_chat="user",
            joined_at=datetime.utcnow()
        )
        db.add(participant)

    db.commit()
    db.close()
    print("✅ Seed completed: user=1, order=1, chat=1, participant=1")

if __name__ == "__main__":
    run_seed()
