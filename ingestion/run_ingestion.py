from seed_sources import seed
from fetcher import fetch_all_sources

if __name__ == "__main__":
    print("🚀 Starting ingestion...")

    # Seed sources into DB if needed
    seed()

    # Fetch all news articles
    fetch_all_sources()

    print("✅ Ingestion completed")