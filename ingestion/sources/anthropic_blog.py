from sources.rss_base import fetch_rss_source

def fetch_anthropic_blog():
    fetch_rss_source(
        feed_url="https://www.anthropic.com/rss.xml",
        source_name="Anthropic Blog",
        default_author="Anthropic",
    )