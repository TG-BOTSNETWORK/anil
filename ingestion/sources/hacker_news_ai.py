import requests
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import NewsItem
from dedup import is_duplicate

SOURCE_NAME = "Hacker News AI"
MAX_ARTICLES = 100
BATCH_SIZE = 20
AI_KEYWORDS = ["artificial intelligence", "machine learning", "llm", "openai",
               "deepmind", "anthropic", "chatgpt", "gpt", "neural network",
               "deep learning", "stable diffusion", "gemini", "claude"]


def fetch_hacker_news_ai():
    db = SessionLocal()
    print(f"[Fetcher] Fetching from source: {SOURCE_NAME}")

    inserted_count = 0
    batch_count = 0
    since_ts = int((datetime.utcnow() - timedelta(days=7)).timestamp())

    for keyword in AI_KEYWORDS:
        if inserted_count >= MAX_ARTICLES:
            break
        try:
            url = (
                f"https://hn.algolia.com/api/v1/search_by_date"
                f"?query={requests.utils.quote(keyword)}"
                f"&tags=story"
                f"&numericFilters=created_at_i>{since_ts},points>5"
                f"&hitsPerPage=20"
            )
            resp = requests.get(url, timeout=10)
            hits = resp.json().get("hits", [])
        except Exception as e:
            print(f"⚠️ HN API error for '{keyword}': {e}")
            continue

        for hit in hits:
            if inserted_count >= MAX_ARTICLES:
                break

            title = hit.get("title", "").strip()
            article_url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
            author = hit.get("author", "HN User")
            summary = hit.get("story_text", "") or ""
            published_at = None
            if hit.get("created_at"):
                try:
                    published_at = datetime.fromisoformat(hit["created_at"].replace("Z", "+00:00"))
                except Exception:
                    pass

            if not article_url or is_duplicate(db, article_url):
                continue

            news = NewsItem(
                source_id=None, title=title, summary=summary[:1000],
                author=author, url=article_url, published_at=published_at,
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