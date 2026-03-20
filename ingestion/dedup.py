from models import NewsItem

def is_duplicate(db, url):
    # ✅ Prevent autoflush crash
    with db.no_autoflush:
        return db.query(NewsItem).filter(NewsItem.url == url).first() is not None