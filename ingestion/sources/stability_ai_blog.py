from sources.rss_base import fetch_rss_source

def fetch_stability_ai_blog():
    fetch_rss_source(
        feed_url="https://stability.ai/news/rss.xml",
        source_name="Stability AI Blog",
        default_author="Stability AI",
    )