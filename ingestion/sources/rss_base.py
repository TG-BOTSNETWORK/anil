import feedparser
import requests
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import NewsItem
from dedup import is_duplicate

HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_ARTICLES = 150
BATCH_SIZE = 20


def fetch_rss_source(feed_url, source_name, default_author="Unknown", ai_filter_keywords=None):
    """Generic RSS fetcher. Pass ai_filter_keywords list to filter only AI-related posts."""
    db = SessionLocal()
    print(f"[Fetcher] Fetching from source: {source_name}")

    try:
        feed = feedparser.parse(feed_url)
        entries = feed.entries
        print(f"ℹ️ Found {len(entries)} entries in {source_name}")
    except Exception as e:
        print(f"⚠️ Error fetching {source_name}: {e}")
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
        author = entry.get("author", default_author).strip()

        # Parse published date
        published_at = None
        if entry.get("published_parsed"):
            try:
                published_at = datetime(*entry.published_parsed[:6])
            except Exception:
                pass

        # Optional: filter by AI keywords for general news sources
        if ai_filter_keywords:
            text = (title + " " + summary).lower()
            if not any(kw in text for kw in ai_filter_keywords):
                continue

        if not url or is_duplicate(db, url):
            continue

        news = NewsItem(
            source_id=None,
            title=title,
            summary=summary[:1000] if summary else "",
            author=author,
            url=url,
            published_at=published_at,
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

    print(f"✅ Inserted {inserted_count} articles from {source_name}")
    db.close()