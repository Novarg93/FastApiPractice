from sqlalchemy.orm import Session
from app.models.chat import ChatRoom, ChatParticipant

def create_chat_for_order(db: Session, order_id: int, client_id: int, booster_id: int | None = None):
    # Room create
    room = ChatRoom(order_id=order_id)
    db.add(room)
    db.flush()

    client_participant = ChatParticipant(
        chat_id=room.id,
        user_id=client_id,
        role_in_chat="user"
    )
    db.add(client_participant)

    if booster_id:
        booster_participant = ChatParticipant(
            chat_id=room.id,
            user_id=booster_id,
            role_in_chat="booster"
        )

    db.commit()
    db.refresh(room)
    return room
