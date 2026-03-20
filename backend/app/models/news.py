from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class NewsItem(Base):
    __tablename__ = "news_items"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    title = Column(String(500), nullable=False)
    summary = Column(Text)
    author = Column(String(200))
    url = Column(String(1000), unique=True, nullable=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cluster_id = Column(Integer, nullable=True)
    ai_summary = Column(Text, nullable=True)
    relevance_score = Column(Float, default=0.0)
    entities = Column(JSON, nullable=True)

    source = relationship("Source", back_populates="news_items")
    favorites = relationship("Favorite", back_populates="news_item")
    broadcast_logs = relationship("BroadcastLog", back_populates="news_item")