from sources.rss_base import fetch_rss_source

def fetch_wired_ai():
    fetch_rss_source(
        feed_url="https://www.wired.com/feed/category/artificial-intelligence/rss",
        source_name="Wired AI",
        default_author="Wired",
    )