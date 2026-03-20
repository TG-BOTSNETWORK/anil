from dotenv import load_dotenv
load_dotenv()

from models.db import SessionLocal
from services.dedup_cluster import score_all_unscored

db = SessionLocal()
print("Scoring articles...")
score_all_unscored(db, batch=500)
db.close()
print("Done.")