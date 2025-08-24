from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.chat import MessageType, Message
from typing import Dict, List
from datetime import datetime


router = APIRouter()

active_connections: Dict[int, List[WebSocket]] = {} # {room_id: "websocket1, websocket2}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def connect(room_id: int, websocket: WebSocket):
    await websocket.accept()
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)

async def disconnect(room_id: int, websocket: WebSocket):
    active_connections[room_id].remove(websocket)
    if not active_connections[room_id]:
        del active_connections[room_id]

async def broadcast(room_id: int, message: dict):
    if room_id in active_connections:
        for conn in active_connections[room_id]:
            await conn.send_json(message)

@router.websocket("/ws/chat/{room_id}")
async def chat_ws(websocket: WebSocket, room_id: int, db: Session = Depends(get_db)):
    await connect(room_id, websocket)

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
            # Сохраняем в БД
            new_msg = Message(
                room_id=room_id,
                sender_id=data["sender_id"],
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

            # Рассылка
            await broadcast(room_id, data)


    except WebSocketDisconnect:
        await disconnect(room_id, websocket)