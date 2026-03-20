from sqlalchemy import text
from app.db.session import engine
from app.db.base import Base


def run_auto_migration():
    try:
        # ✅ create tables if not exist
        Base.metadata.create_all(bind=engine)
        print("[DB] ✅ Tables ready")

        # ✅ FORCE SAFE MIGRATIONS (no inspector)
        with engine.begin() as conn:

            # USERS
            conn.execute(text(
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS password VARCHAR(500)"
            ))

            # SOURCES
            conn.execute(text(
                "ALTER TABLE sources ADD COLUMN IF NOT EXISTS category VARCHAR(100)"
            ))

            # NEWS
            conn.execute(text(
                "ALTER TABLE news_items ADD COLUMN IF NOT EXISTS ai_summary TEXT"
            ))

            conn.execute(text(
                "ALTER TABLE news_items ADD COLUMN IF NOT EXISTS relevance_score FLOAT DEFAULT 0.0"
            ))

            conn.execute(text(
                "ALTER TABLE news_items ADD COLUMN IF NOT EXISTS cluster_id INTEGER"
            ))

            conn.execute(text(
                "ALTER TABLE news_items ADD COLUMN IF NOT EXISTS entities JSONB"
            ))

        print("[DB] ✅ Migration done (safe mode)")

    except Exception as e:
        print("[DB ERROR]", e)