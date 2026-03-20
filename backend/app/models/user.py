from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(300), unique=True, nullable=False)
    name = Column(String(200))

    # ✅ REQUIRED (fixes your error)
    password = Column(String(500), nullable=False)

    linkedin_handle = Column(String(200), nullable=True)
    whatsapp_number = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    favorites = relationship("Favorite", back_populates="user")
    broadcast_logs = relationship("BroadcastLog", back_populates="user")