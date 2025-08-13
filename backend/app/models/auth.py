from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime
from app.database.session import Base

class BlacklistedToken(Base):
    __tablename__ = "token_blacklist"

    jti = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
