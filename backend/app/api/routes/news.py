from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services.news_service import get_news, get_source_summary
from app.db.session import get_db
from app.core.deps import get_current_user
from app.services.news_service import get_news_by_id


router = APIRouter()

@router.get("/")
def fetch_news(
    keyword: str = Query(None),
    source_id: int = Query(None),
    sort_by: str = Query("impact"),
    page: int = Query(1, ge=1),
    page_size: int = Query(40, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = get_news(db, user.id, keyword, source_id, sort_by, page, page_size)
    return {"data": data, "page": page, "page_size": page_size}

@router.get("/sources")
def source_summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Return summarized info per source
    """
    return get_source_summary(db, user.id)

@router.get("/{news_id}")
def fetch_news_by_id(news_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Fetch a single news item by ID.
    Only returns: title, ai_summary, url
    """
    return {"data": get_news_by_id(db, news_id, user.id)}