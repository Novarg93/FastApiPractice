"""add chat tables

Revision ID: b43fc6622bcd
Revises: e871cfe6457b
Create Date: 2025-08-24 16:41:11.109747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b43fc6622bcd'
down_revision: Union[str, Sequence[str], None] = 'e871cfe6457b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Enum для сообщений
    message_type = sa.Enum("text", "media", "system", name="messagetype")
    message_type.create(op.get_bind(), checkfirst=True)

    # Enum для ролей пользователей
    user_role = sa.Enum("user", "booster", "support", "admin", name="userrole")
    user_role.create(op.get_bind(), checkfirst=True)

    # Добавляем колонку role в таблицу users
    op.add_column("users", sa.Column("role", user_role, nullable=False, server_default="user"))

    # ChatRoom
    op.create_table(
        "chat_rooms",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sqlite_autoincrement=True,
    )

    # ChatParticipants
    op.create_table(
        "chat_participants",
        sa.Column("chat_id", sa.Integer, sa.ForeignKey("chat_rooms.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("role_in_chat", sa.String(length=50), nullable=False, server_default="user"),
        sa.Column("joined_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

    # Messages
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("room_id", sa.Integer, sa.ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False),
        sa.Column("sender_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", message_type, nullable=False, server_default="text"),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sqlite_autoincrement=True,
    )


def downgrade() -> None:
    op.drop_table("messages")
    op.drop_table("chat_participants")
    op.drop_table("chat_rooms")

    # Убираем колонку role у users
    op.drop_column("users", "role")

    # Удаляем enum
    user_role = sa.Enum("user", "booster", "support", "admin", name="userrole")
    user_role.drop(op.get_bind(), checkfirst=True)

    message_type = sa.Enum("text", "media", "system", name="messagetype")
    message_type.drop(op.get_bind(), checkfirst=True)
