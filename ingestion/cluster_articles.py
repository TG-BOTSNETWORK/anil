from dotenv import load_dotenv
load_dotenv()

from models.db import SessionLocal
from services.dedup_cluster import cluster_news_items

db = SessionLocal()
print("Clustering articles...")
cluster_news_items(db, threshold=0.25, limit=500)
db.close()
print("Done.")