from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List

from app.database.session import SessionLocal
from app.models.chat import MessageType, Message, ChatParticipant
from app.models.users import User, UserRole
from app.core.security import get_current_user
from app.schemas.chat import MessageRead

router = APIRouter()

active_connections: Dict[int, List[WebSocket]] = {}  # {room_id: [websocket1, websocket2]}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def user_can_access_chat(db: Session, room_id: int, current_user: User) -> bool:
    # Админ и саппорт видят все чаты
    if current_user.role in [UserRole.ADMIN, UserRole.SUPPORT]:
        return True

    # Юзер/бустер — только если участвуют в чате
    participant = (
        db.query(ChatParticipant)
        .filter_by(chat_id=room_id, user_id=current_user.id)
        .first()
    )
    return participant is not None


async def connect(room_id: int, websocket: WebSocket):
    await websocket.accept()
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)


async def disconnect(room_id: int, websocket: WebSocket):
    active_connections[room_id].remove(websocket)
    if not active_connections[room_id]:
        del active_connections[room_id]


async def broadcast(room_id: int, message: MessageRead):
    if room_id in active_connections:
        for conn in active_connections[room_id]:
            await conn.send_json(message)


@router.websocket("/ws/chat/{room_id}")
async def chat_ws(
    websocket: WebSocket,
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Проверяем доступ
    if not user_can_access_chat(db, room_id, current_user):
        await websocket.close(code=1008)
        return

    await connect(room_id, websocket)

    # Загружаем историю сообщений
    history = (
        db.query(Message)
        .filter(Message.room_id == room_id)
        .order_by(Message.created_at.asc())
        .all()
    )
    for msg in history:
        await websocket.send_json(
            {
                "id": msg.id,
                "sender_id": msg.sender_id,
                "content": msg.content,
                "type": msg.type.value,
                "created_at": msg.created_at.isoformat(),
            }
        )

    try:
        while True:
            data = await websocket.receive_json()

            # Сохраняем новое сообщение
            new_msg = Message(
                room_id=room_id,
                sender_id=current_user.id,
                type=MessageType.text,
                content=data["content"],
                created_at=datetime.utcnow(),
            )
            db.add(new_msg)
            db.commit()
            db.refresh(new_msg)

            msg_dict = {
                "id": new_msg.id,
                "sender_id": new_msg.sender_id,
                "content": new_msg.content,
                "type": new_msg.type.value,
                "created_at": new_msg.created_at.isoformat(),
            }

            # Рассылаем всем в комнате
            await broadcast(room_id, msg_dict)

    except WebSocketDisconnect:
        await disconnect(room_id, websocket)
