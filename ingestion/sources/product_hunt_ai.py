import requests
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import NewsItem
from dedup import is_duplicate

SOURCE_NAME = "Product Hunt AI"
# Product Hunt has a public RSS feed for the AI topic
FEED_URL = "https://www.producthunt.com/feed?category=artificial-intelligence"
HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_ARTICLES = 100
BATCH_SIZE = 20


def fetch_product_hunt_ai():
    import feedparser
    db = SessionLocal()
    print(f"[Fetcher] Fetching from source: {SOURCE_NAME}")

    try:
        feed = feedparser.parse(FEED_URL)
        entries = feed.entries
        print(f"ℹ️ Found {len(entries)} entries in {SOURCE_NAME}")
    except Exception as e:
        print(f"⚠️ Error fetching {SOURCE_NAME}: {e}")
        db.close()
        return

    inserted_count = 0
    batch_count = 0

    for entry in entries:
        if inserted_count >= MAX_ARTICLES:
            break

        title = entry.get("title", "No Title").strip()
        url = entry.get("link", None)
        summary = entry.get("summary", "").strip()
        author = entry.get("author", "Product Hunt")
        published_at = None
        if entry.get("published_parsed"):
            try:
                published_at = datetime(*entry.published_parsed[:6])
            except Exception:
                pass

        if not url or is_duplicate(db, url):
            continue

        news = NewsItem(
            source_id=None, title=title, summary=summary[:1000],
            author=author, url=url, published_at=published_at,
        )
        try:
            db.add(news)
            inserted_count += 1
            batch_count += 1
            if batch_count % BATCH_SIZE == 0:
                db.commit()
                batch_count = 0
        except IntegrityError:
            db.rollback()

    if batch_count > 0:
        db.commit()
    print(f"✅ Inserted {inserted_count} articles from {SOURCE_NAME}")
    db.close()