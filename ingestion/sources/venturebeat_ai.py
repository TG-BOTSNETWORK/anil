from sources.rss_base import fetch_rss_source

def fetch_venturebeat_ai():
    fetch_rss_source(
        feed_url="https://venturebeat.com/category/ai/feed/",
        source_name="VentureBeat AI",
        default_author="VentureBeat",
    )