from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List

from app.db.session import get_db
from app.models.news import NewsItem
from app.models.broadcast import BroadcastLog
from app.services.broadcast_service import broadcast_news
from app.core.deps import get_current_user

router = APIRouter()


# -------------------------------
# ✅ REQUEST SCHEMA (IMPORTANT)
# -------------------------------
class BroadcastRequest(BaseModel):
    news_id: int = Field(..., gt=0)
    channels: List[str] = Field(..., min_items=1)


# -------------------------------
# ✅ RESPONSE SCHEMA (OPTIONAL)
# -------------------------------
class BroadcastResponse(BaseModel):
    msg: str
    results: List[dict]


# -------------------------------
# ✅ BROADCAST API
# -------------------------------
@router.post("/", response_model=BroadcastResponse, status_code=status.HTTP_200_OK)
def broadcast(
    data: BroadcastRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        # 🔍 Fetch news
        news = db.query(NewsItem).filter(NewsItem.id == data.news_id).first()

        if not news:
            raise HTTPException(status_code=404, detail="News not found")

        # 🚀 Send broadcast
        results = broadcast_news(news, data.channels, user)

        # 🧾 Store logs
        for res in results:
            db.add(BroadcastLog(
                user_id=user.id,
                news_item_id=data.news_id,
                channel=res.get("channel"),
                status=res.get("status", "unknown"),
                payload=res
            ))

        db.commit()

        return {
            "msg": "Broadcast completed",
            "results": results
        }

    except Exception as e:
        db.rollback()  # ✅ Important for DB safety
        raise HTTPException(
            status_code=500,
            detail=f"Broadcast failed: {str(e)}"
        )