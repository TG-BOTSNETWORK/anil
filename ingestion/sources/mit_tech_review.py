from sources.rss_base import fetch_rss_source

def fetch_mit_tech_review():
    fetch_rss_source(
        feed_url="https://www.technologyreview.com/topic/artificial-intelligence/feed",
        source_name="MIT Technology Review",
        default_author="MIT Technology Review",
    )