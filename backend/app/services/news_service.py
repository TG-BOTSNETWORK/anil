from sqlalchemy.orm import Session, joinedload
from app.models.news import NewsItem
from app.models.favorite import Favorite
from sqlalchemy import func


def get_news(
    db: Session,
    user_id: int,
    keyword: str = None,
    source_id: int = None,
    sort_by: str = "impact",
    page: int = 1,
    page_size: int = 40
):
    query = db.query(NewsItem).options(joinedload(NewsItem.source))

    # 🔍 Search
    if keyword:
        query = query.filter(NewsItem.title.ilike(f"%{keyword}%"))

    # 🔎 Filter by source
    if source_id:
        query = query.filter(NewsItem.source_id == source_id)

    # 🔥 Sorting
    if sort_by == "impact":
        query = query.order_by(NewsItem.relevance_score.desc())
    elif sort_by == "published_at":
        query = query.order_by(NewsItem.published_at.desc())
    elif sort_by == "source_activity":
        # Sort by how many news items each source has
        subquery = (
            db.query(NewsItem.source_id, func.count(NewsItem.id).label("count"))
            .group_by(NewsItem.source_id)
            .subquery()
        )
        query = query.join(subquery, NewsItem.source_id == subquery.c.source_id)
        query = query.order_by(subquery.c.count.desc())
    else:
        query = query.order_by(NewsItem.published_at.desc())

    # 📄 Pagination
    offset = (page - 1) * page_size
    news_list = query.offset(offset).limit(page_size).all()

    # ⭐ Mark favorites
    fav_ids = {f.news_item_id for f in db.query(Favorite).filter(Favorite.user_id == user_id).all()}

    # Format response
    result = []
    for n in news_list:
        result.append({
            "id": n.id,
            "title": n.title,
            "summary": n.summary,
            "ai_summary": n.ai_summary,
            "source": n.source.name if n.source else "Unknown",
            "source_id": n.source_id,
            "published_at": n.published_at,
            "cluster_id": n.cluster_id,
            "relevance_score": n.relevance_score,
            "is_favorited": n.id in fav_ids
        })

    return result


def get_source_summary(db: Session, user_id: int):
    """
    Summarize news per source for charts (e.g., news count and favorites count per source)
    """
    query = (
        db.query(
            NewsItem.source_id,
            NewsItem.source,
            func.count(NewsItem.id).label("news_count"),
            func.sum(
                func.case([(Favorite.news_item_id != None, 1)], else_=0)
            ).label("favorite_count")
        )
        .outerjoin(Favorite, (Favorite.news_item_id == NewsItem.id) & (Favorite.user_id == user_id))
        .group_by(NewsItem.source_id, NewsItem.source)
        .all()
    )

    result = []
    for s in query:
        result.append({
            "source_id": s.source_id,
            "source": s.source if s.source else "Unknown",
            "news_count": s.news_count,
            "favorite_count": int(s.favorite_count)
        })
    return result


def get_news_by_id(db: Session, news_id: int, user_id: int):
    # Fetch the news item by id (no need to filter by user_id if not needed)
    news_item = db.query(NewsItem).filter(NewsItem.id == news_id).first()
    if not news_item:
        raise HTTPException(status_code=404, detail="News not found")

    # Only return title, ai_summary, and url
    return {
        "id": news_item.id,
        "title": news_item.title,
        "ai_summary": news_item.ai_summary,
        "url": news_item.url
    }