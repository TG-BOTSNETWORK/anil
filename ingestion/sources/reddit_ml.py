import requests
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import NewsItem
from dedup import is_duplicate

SOURCE_NAME = "Reddit r/MachineLearning"
SUBREDDIT_URL = "https://www.reddit.com/r/MachineLearning/hot.json?limit=50"
HEADERS = {"User-Agent": "Mozilla/5.0 AI News Fetcher/1.0"}
MAX_ARTICLES = 100
BATCH_SIZE = 20


def fetch_reddit_ml():
    db = SessionLocal()
    print(f"[Fetcher] Fetching from source: {SOURCE_NAME}")

    try:
        resp = requests.get(SUBREDDIT_URL, headers=HEADERS, timeout=10)
        posts = resp.json()["data"]["children"]
        print(f"ℹ️ Found {len(posts)} posts from {SOURCE_NAME}")
    except Exception as e:
        print(f"⚠️ Error fetching {SOURCE_NAME}: {e}")
        db.close()
        return

    inserted_count = 0
    batch_count = 0

    for post in posts:
        if inserted_count >= MAX_ARTICLES:
            break

        data = post["data"]
        if data.get("stickied") or data.get("is_video"):
            continue

        title = data.get("title", "").strip()
        url = data.get("url", "")
        # Use the Reddit post URL if the linked URL is a Reddit self-post
        if "reddit.com" in url or not url:
            url = f"https://www.reddit.com{data.get('permalink', '')}"
        author = data.get("author", "redditor")
        summary = data.get("selftext", "")[:1000]
        published_at = None
        if data.get("created_utc"):
            published_at = datetime.utcfromtimestamp(data["created_utc"])

        if not url or is_duplicate(db, url):
            continue

        news = NewsItem(
            source_id=None, title=title, summary=summary,
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