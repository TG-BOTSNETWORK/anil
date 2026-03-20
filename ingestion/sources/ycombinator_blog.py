from sources.rss_base import fetch_rss_source

def fetch_ycombinator_blog():
    fetch_rss_source(
        feed_url="https://www.ycombinator.com/blog/rss.xml",
        source_name="Y Combinator Blog",
        default_author="Y Combinator",
        ai_filter_keywords=["ai", "llm", "machine learning", "gpt", "model", "neural"],
    )