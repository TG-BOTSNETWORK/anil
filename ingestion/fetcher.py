from sources.openai_blog import fetch_openai_blog
from sources.google_ai_blog import fetch_google_ai_blog
from sources.meta_ai_blog import fetch_meta_ai_blog
from sources.anthropic_blog import fetch_anthropic_blog
from sources.microsoft_ai_blog import fetch_microsoft_ai_blog
from sources.stability_ai_blog import fetch_stability_ai_blog
from sources.ycombinator_blog import fetch_ycombinator_blog
from sources.techcrunch_ai import fetch_techcrunch_ai
from sources.venturebeat_ai import fetch_venturebeat_ai
from sources.theverge_tech import fetch_theverge_tech
from sources.wired_ai import fetch_wired_ai
from sources.mit_tech_review import fetch_mit_tech_review
from sources.paperswithcode import fetch_paperswithcode
from sources.hacker_news_ai import fetch_hacker_news_ai
from sources.reddit_ml import fetch_reddit_ml
from sources.product_hunt_ai import fetch_product_hunt_ai
# These you already have:
# from sources.huggingface_blog import fetch_huggingface_blog
# from sources.deepmind_blog import fetch_deepmind_blog
# from sources.arxiv import fetch_arxiv


def fetch_all_sources():
    print("🚀 Starting fetching all sources...")
    fetch_openai_blog()
    fetch_google_ai_blog()
    fetch_meta_ai_blog()
    fetch_anthropic_blog()
    fetch_microsoft_ai_blog()
    fetch_stability_ai_blog()
    fetch_ycombinator_blog()
    fetch_techcrunch_ai()
    fetch_venturebeat_ai()
    fetch_theverge_tech()
    fetch_wired_ai()
    fetch_mit_tech_review()
    fetch_paperswithcode()
    fetch_hacker_news_ai()
    fetch_reddit_ml()
    fetch_product_hunt_ai()
    # fetch_huggingface_blog()
    # fetch_deepmind_blog()
    # fetch_arxiv()
    print("✅ All sources fetched successfully")