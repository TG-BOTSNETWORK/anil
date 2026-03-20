"""
summarize_articles.py
Fully populates the news_items table:
- Fills missing author, summary, ai_summary, and entities
- Uses Anthropic API via ai_service (with title fallback when credits are low)
- Computes relevance_score and cluster_id for all articles
- Stops making API calls immediately if credit balance is exhausted
"""

import os
import time
import traceback
from dotenv import load_dotenv
load_dotenv()

from models.db import SessionLocal, NewsItem
from services.ai_service import generate_ai_summary, extract_entities, _credits_exhausted
from services.dedup_cluster import score_relevance

# ── Source name → default author ─────────────────────────────────────────────
SOURCE_AUTHORS = {
    "openai_blog":        "OpenAI",
    "google_ai_blog":     "Google AI",
    "meta_ai_blog":       "Meta AI",
    "anthropic_blog":     "Anthropic",
    "microsoft_ai_blog":  "Microsoft AI",
    "stability_ai_blog":  "Stability AI",
    "ycombinator_blog":   "Y Combinator",
    "techcrunch_ai":      "TechCrunch AI",
    "venturebeat_ai":     "VentureBeat AI",
    "theverge_tech":      "The Verge",
    "wired_ai":           "Wired",
    "mit_tech_review":    "MIT Technology Review",
    "paperswithcode":     "Papers With Code",
    "hacker_news_ai":     "Hacker News",
    "reddit_ml":          "Reddit ML",
    "product_hunt_ai":    "Product Hunt",
}

FALLBACK_SUMMARY = "No summary available."


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_source_name(item: NewsItem) -> str:
    """Safely reads Source.name from the relationship without writing to it."""
    try:
        src = item.source
        if src is not None:
            return (src.name or "").strip()
    except Exception:
        pass
    return ""


def safe_extract_entities(text: str) -> list:
    """Calls extract_entities() and guarantees a list[str|dict] is returned."""
    try:
        result = extract_entities(text)
        if not result:
            return []
        if isinstance(result, str):
            return [e.strip() for e in result.split(",") if e.strip()]
        if isinstance(result, (list, tuple)):
            return list(result)
        return []
    except Exception as e:
        print(f"    ⚠️  Entity extraction error: {e}")
        return []


# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    # Import the live flag (re-import so we always see the current value)
    import services.ai_service as ai_svc

    db = SessionLocal()
    articles = db.query(NewsItem).order_by(NewsItem.id.desc()).all()
    total = len(articles)
    print(f"Processing {total} articles in the database...\n")

    success = 0
    failed  = 0

    for i, item in enumerate(articles, 1):
        title_short   = (item.title or "?")[:60]
        current_field = "init"
        try:
            # ── 1. author ──────────────────────────────────────────────────
            current_field = "author"
            if not item.author:
                source_name = get_source_name(item)
                item.author = SOURCE_AUTHORS.get(source_name, "Unknown")

            # ── 2. Base text ───────────────────────────────────────────────
            current_field = "base_text"
            base_text = (item.summary or "").strip() or (item.title or "").strip()

            if not base_text:
                item.summary    = FALLBACK_SUMMARY
                item.ai_summary = FALLBACK_SUMMARY
                item.entities   = []
                db.commit()
                failed += 1
                print(f"[{i}/{total}] ⚠️  '{title_short}' – no text, fallbacks written")
                continue

            # ── 3. summary ─────────────────────────────────────────────────
            # When credits are exhausted, generate_ai_summary returns the raw
            # text[:300] as fallback — no blank values left behind.
            current_field = "summary"
            if not item.summary:
                item.summary = generate_ai_summary(base_text)

            # ── 4. ai_summary ──────────────────────────────────────────────
            current_field = "ai_summary"
            if not item.ai_summary:
                item.ai_summary = generate_ai_summary(item.summary or base_text)

            # ── 5. entities ────────────────────────────────────────────────
            current_field = "entities"
            if not item.entities:
                item.entities = safe_extract_entities(item.summary or base_text)

            # ── 6. commit ──────────────────────────────────────────────────
            current_field = "db.commit"
            db.commit()

            success += 1
            print(f"✅ [{i}/{total}] '{title_short}' updated")

            # Skip sleep when credits are gone — no API calls being made
            if not ai_svc._credits_exhausted:
                time.sleep(0.3)

        except Exception as e:
            db.rollback()
            try:
                db.expire(item)
            except Exception:
                pass
            failed += 1
            print(
                f"❌ [{i}/{total}] FAILED at field='{current_field}' "
                f"on '{title_short}': {e}"
            )
            if failed <= 5:
                traceback.print_exc()

    print(f"\n── AI Summary & Entities ──────────────────────")
    print(f"  ✅ Success : {success}")
    print(f"  ⚠️  Failed  : {failed}")
    print(f"  Total     : {total}")
    print(f"───────────────────────────────────────────────\n")

    # ── 7. Relevance scores ────────────────────────────────────────────────
    print("Scoring relevance for all articles...")
    for item in articles:
        text = item.summary or item.title or ""
        if text:
            item.relevance_score = score_relevance(item.title or "", text)
    db.commit()
    print("✅ Relevance scoring complete.")

    # ── 8. Cluster ALL articles in batches of 500 ────────────────────────
    # cluster_news_items() fetches only the top `limit` rows, so articles
    # beyond position 500 are never touched. We page through the full table
    # with an offset so every article gets a cluster_id.
    from services.dedup_cluster import _tokenize, _tfidf_vectors, _cosine_sim

    all_count = db.query(NewsItem).count()
    print(f"\nClustering all {all_count} articles in batches of 500...")

    BATCH      = 500
    THRESHOLD  = 0.25
    offset     = 0
    batch_num  = 0

    while offset < all_count:
        batch_num += 1
        items = (
            db.query(NewsItem)
            .order_by(NewsItem.id.desc())
            .offset(offset)
            .limit(BATCH)
            .all()
        )
        if not items:
            break

        texts   = [_tokenize(f"{i.title} {i.summary or ''}") for i in items]
        vectors = _tfidf_vectors(texts)

        # Use globally unique cluster IDs so batches don't collide
        cluster_map  = {}
        next_cluster = (batch_num - 1) * BATCH + 1

        for i in range(len(items)):
            if items[i].id in cluster_map:
                continue
            cluster_map[items[i].id] = next_cluster
            for j in range(i + 1, len(items)):
                if items[j].id in cluster_map:
                    continue
                if _cosine_sim(vectors[i], vectors[j]) >= THRESHOLD:
                    cluster_map[items[j].id] = next_cluster
            next_cluster += 1

        for item in items:
            item.cluster_id = cluster_map.get(item.id)

        db.commit()
        print(f"  ✅ Batch {batch_num}: articles {offset + 1}–{offset + len(items)}")
        offset += BATCH

    print(f"✅ Clustering complete — {batch_num} batch(es), all {all_count} articles assigned.")

    db.close()
    print("\n✅ Full update complete. All table values filled automatically.")


if __name__ == "__main__":
    run() 