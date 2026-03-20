from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class BroadcastLog(Base):
    __tablename__ = "broadcast_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    news_item_id = Column(Integer, ForeignKey("news_items.id"), nullable=False)

    channel = Column(String(50), nullable=False)
    status = Column(String(50), default="sent")
    payload = Column(JSON, nullable=True)

    sent_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="broadcast_logs")
    news_item = relationship("NewsItem", back_populates="broadcast_logs")