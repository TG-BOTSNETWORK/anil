from sources.rss_base import fetch_rss_source

def fetch_microsoft_ai_blog():
    fetch_rss_source(
        feed_url="https://blogs.microsoft.com/ai/feed/",
        source_name="Microsoft AI Blog",
        default_author="Microsoft",
    )