import os

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List
from jose import jwt, JWTError

from app.core.security import get_current_user
from app.core.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.session import SessionLocal
from app.models.chat import MessageType, Message, ChatParticipant, ChatRoom
from app.models.users import User, UserRole
from app.schemas.chat import MessageRead

router = APIRouter()

# Активные подключения: {room_id: [ws1, ws2]}
active_connections: Dict[int, List[WebSocket]] = {}


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
    # Обычный юзер/бустер — только если участвуют в чате
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


def get_current_user_ws(db: Session, websocket: WebSocket):
    """Пробуем достать токен из заголовка Authorization или query param ?token="""
    token = None

    # 1️⃣ Authorization: Bearer <token>
    auth_header = websocket.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    # 2️⃣ Если нет — из query
    if not token:
        token = websocket.query_params.get("token")

    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            return None
        return db.query(User).filter(User.id == int(user_id)).first()
    except JWTError:
        return None


@router.websocket("/ws/chat/{room_id}")
async def chat_ws(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    # 1️⃣ Авторизация
    current_user = get_current_user_ws(db, websocket)
    if not current_user:
        await websocket.close(code=1008)
        return

    # 2️⃣ Проверка доступа
    if not user_can_access_chat(db, room_id, current_user):
        await websocket.close(code=1008)
        return

    # 3️⃣ Подключение
    await connect(room_id, websocket)

    # 4️⃣ Отдаём историю сообщений
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

    # 5️⃣ Основной цикл
    try:
        while True:
            data = await websocket.receive_json()

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

            await broadcast(room_id, msg_dict)

    except WebSocketDisconnect:
        await disconnect(room_id, websocket)

@router.get("/my/chats")
def get_my_chats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chats = (
        db.query(ChatRoom)
        .join(ChatParticipant)
        .filter(ChatParticipant.user_id == current_user.id)
        .all()
    )

    return [
        {
            "chat_id": c.id,
            "order_id": c.order_id,
            "last_message": c.messages[-1].content if c.messages else None,
            "updated_at": c.messages[-1].created_at if c.messages else c.created_at,
        }
        for c in chats
    ]

@router.patch("/chats/{chat_id}/messages/{msg_id}")
def edit_message(
    chat_id: int,
    msg_id: int,
    new_content: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    msg = db.query(Message).filter(
        Message.id == msg_id,
        Message.room_id == chat_id
    ).first()

    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    # Только ADMIN и SUPPORT могут редактировать
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPPORT]:
        raise HTTPException(status_code=403, detail="Permission denied")

    msg.content = new_content
    db.commit()
    db.refresh(msg)

    return {
        "id": msg.id,
        "sender_id": msg.sender_id,
        "content": msg.content,
        "type": msg.type.value,
        "created_at": msg.created_at.isoformat()
    }
