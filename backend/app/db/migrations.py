from sqlalchemy import inspect, text
from app.db.session import engine
from app.db.base import Base

def run_auto_migration():
    try:
        Base.metadata.create_all(bind=engine)
        print("[DB] ✅ Tables ready")

        inspector = inspect(engine)

        with engine.begin() as conn:
            # SOURCES
            sources_cols = {c["name"] for c in inspector.get_columns("sources")}
            if "category" not in sources_cols:
                conn.execute(text("ALTER TABLE sources ADD COLUMN category VARCHAR(100)"))

            # NEWS
            news_cols = {c["name"] for c in inspector.get_columns("news_items")}
            if "ai_summary" not in news_cols:
                conn.execute(text("ALTER TABLE news_items ADD COLUMN ai_summary TEXT"))

        print("[DB] ✅ Migration done")

    except Exception as e:
        print("[DB ERROR]", e)