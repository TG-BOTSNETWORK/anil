# favorites.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.favorite import Favorite
from app.models.news import NewsItem
from app.core.deps import get_current_user
from app.services.favorite_service import toggle_favorite

router = APIRouter(tags=["Favorites"])

@router.post("/")
def toggle_fav(news_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        status = toggle_favorite(db, user.id, news_id)
        return {
            "msg": "added to favorites" if status else "removed from favorites",
            "is_favorite": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_favorites(db: Session = Depends(get_db), user=Depends(get_current_user)):
    favorites = (
        db.query(Favorite, NewsItem)
        .join(NewsItem, Favorite.news_item_id == NewsItem.id)
        .filter(Favorite.user_id == user.id)
        .all()
    )

    result = [
        {
            "favorite_id": fav.id,
            "news_id": news.id,
            "title": news.title,
            "summary": news.summary,
            "source": news.source.name if news.source else None,  # optional
            "url": news.url,
            "published_at": news.published_at,  # ✅ use correct field
            "created_at": news.created_at
        }
        for fav, news in favorites
    ]

    return {
        "count": len(result),
        "data": result
    }