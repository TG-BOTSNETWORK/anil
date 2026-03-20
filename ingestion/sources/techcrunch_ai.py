from sources.rss_base import fetch_rss_source

def fetch_techcrunch_ai():
    fetch_rss_source(
        feed_url="https://techcrunch.com/category/artificial-intelligence/feed/",
        source_name="TechCrunch AI",
        default_author="TechCrunch",
    )