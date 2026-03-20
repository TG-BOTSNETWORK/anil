from sources.rss_base import fetch_rss_source

def fetch_google_ai_blog():
    fetch_rss_source(
        feed_url="https://research.google/blog/rss",
        source_name="Google AI Blog",
        default_author="Google Research",
    )