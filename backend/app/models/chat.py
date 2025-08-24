from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum


class MessageType(str, enum.Enum):
    text = "text"
    media = "media"
    system = "system"


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # связи
    participants = relationship("ChatParticipant", back_populates="chat", cascade="all, delete")
    messages = relationship("Message", back_populates="room", cascade="all, delete")


class ChatParticipant(Base):
    __tablename__ = "chat_participants"

    chat_id = Column(Integer, ForeignKey("chat_rooms.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_in_chat = Column(String(50), nullable=False, server_default="user") # user / booster / support / admin
    joined_at = Column(DateTime, server_default=func.now(), nullable=False)

    # связи
    chat = relationship("ChatRoom", back_populates="participants")
    user = relationship("User", back_populates="chat_participations")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum(MessageType), nullable=False, server_default="text")
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # связи
    room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("User", back_populates="messages")