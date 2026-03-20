from sources.rss_base import fetch_rss_source

def fetch_paperswithcode():
    fetch_rss_source(
        feed_url="https://paperswithcode.com/rss",
        source_name="Papers With Code",
        default_author="Papers With Code",
    )