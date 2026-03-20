import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from db import SessionLocal
from models import NewsItem
from dedup import is_duplicate

HEADERS = {"User-Agent": "Mozilla/5.0"}
SOURCE_NAME = "Meta AI Blog"
SITEMAP_URL = "https://ai.meta.com/sitemap.xml"
BLOG_PREFIX = "https://ai.meta.com/blog/"
MAX_ARTICLES = 150
BATCH_SIZE = 20


def fetch_meta_ai_blog():
    db = SessionLocal()
    print(f"[Fetcher] Fetching from source: {SOURCE_NAME}")

    try:
        resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "xml")
        blog_urls = [
            loc.text.strip() for loc in soup.find_all("loc")
            if loc.text.strip().startswith(BLOG_PREFIX)
            and loc.text.strip() != BLOG_PREFIX
        ]
        print(f"ℹ️ Found {len(blog_urls)} blog URLs from {SOURCE_NAME}")
    except Exception as e:
        print(f"⚠️ Error fetching sitemap for {SOURCE_NAME}: {e}")
        db.close()
        return

    inserted_count = 0
    batch_count = 0

    for url in blog_urls:
        if inserted_count >= MAX_ARTICLES:
            break
        if is_duplicate(db, url):
            continue

        slug = url.rstrip("/").split("/")[-1]
        title = slug.replace("-", " ").title()
        summary = ""

        try:
            page = requests.get(url, headers=HEADERS, timeout=10)
            if page.status_code == 200:
                ps = BeautifulSoup(page.text, "html.parser")
                og_title = ps.find("meta", property="og:title")
                if og_title and og_title.get("content"):
                    title = og_title["content"].strip()
                og_desc = ps.find("meta", property="og:description")
                if og_desc and og_desc.get("content"):
                    summary = og_desc["content"].strip()
        except Exception:
            pass

        news = NewsItem(
            source_id=None, title=title, summary=summary,
            author="Meta AI", url=url, published_at=None
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