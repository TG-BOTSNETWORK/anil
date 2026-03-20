from sources.rss_base import fetch_rss_source

AI_KEYWORDS = ["ai", "artificial intelligence", "llm", "openai", "deepmind", "anthropic",
               "machine learning", "chatgpt", "gemini", "claude", "gpt", "neural"]

def fetch_theverge_tech():
    fetch_rss_source(
        feed_url="https://www.theverge.com/rss/index.xml",
        source_name="The Verge Tech",
        default_author="The Verge",
        ai_filter_keywords=AI_KEYWORDS,
    )