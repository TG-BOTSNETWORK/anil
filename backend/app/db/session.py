import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Retry loop for network issues
max_retries = 5
for attempt in range(max_retries):
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            connect_args={
                "sslmode": "require",
                "connect_timeout": 10
            }
        )
        conn = engine.connect()  # Test DB connection
        conn.close()
        print("✅ Database connected successfully")
        break
    except Exception as e:
        print(f"[DB ERROR] {e}, retrying in 5s... ({attempt+1}/{max_retries})")
        time.sleep(5)
else:
    raise Exception(f"Could not connect to database after {max_retries} attempts")

# SQLAlchemy session
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()