import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import IntegrityError
from db import SessionLocal
from models import NewsItem
from dedup import is_duplicate

HEADERS = {"User-Agent": "Mozilla/5.0"}
MAX_ARTICLES = 150
BATCH_SIZE = 20

SOURCE_NAME = "OpenAI Blog"
# Sub-sitemap that actually contains blog/index articles
SITEMAP_URL = "https://openai.com/sitemap.xml/product/"
BLOG_PREFIX = "https://openai.com/index/"


def fetch_openai_blog():
    db = SessionLocal()
    print(f"[Fetcher] Fetching from source: {SOURCE_NAME}")

    try:
        response = requests.get(SITEMAP_URL, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch sitemap, status code: {response.status_code}")
            db.close()
            return

        soup = BeautifulSoup(response.text, "xml")
        all_urls = [loc.text.strip() for loc in soup.find_all("loc")]

        # Filter to blog/index article URLs only
        blog_urls = [u for u in all_urls if u.startswith(BLOG_PREFIX)]
        print(f"ℹ️ Found {len(blog_urls)} blog URLs from sitemap")

    except Exception as e:
        print(f"⚠️ Error fetching sitemap: {e}")
        db.close()
        return

    if not blog_urls:
        print("⚠️ No blog URLs found.")
        db.close()
        return

    inserted_count = 0
    batch_count = 0

    for url in blog_urls:
        if inserted_count >= MAX_ARTICLES:
            break

        if is_duplicate(db, url):
            continue

        # Fallback title from URL slug
        slug = url.rstrip("/").split("/")[-1]
        title = slug.replace("-", " ").title()
        summary = ""

        # Fetch real title and description from og: meta tags
        try:
            page = requests.get(url, headers=HEADERS, timeout=10)
            if page.status_code == 200:
                page_soup = BeautifulSoup(page.text, "html.parser")

                og_title = page_soup.find("meta", property="og:title")
                if og_title and og_title.get("content"):
                    title = og_title["content"].strip()

                og_desc = page_soup.find("meta", property="og:description")
                if og_desc and og_desc.get("content"):
                    summary = og_desc["content"].strip()
        except Exception as e:
            print(f"⚠️ Could not fetch {url}: {e}")

        news = NewsItem(
            source_id=None,
            title=title,
            summary=summary,
            author="OpenAI",
            url=url,
            published_at=None
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


if __name__ == "__main__":
    fetch_openai_blog()