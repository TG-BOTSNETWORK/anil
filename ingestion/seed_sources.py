from db import SessionLocal, Base, engine
from models import Source
from sources import SOURCES

def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    for src in SOURCES:
        exists = db.query(Source).filter(Source.name == src["name"]).first()

        if not exists:
            db.add(Source(
                name=src["name"],
                rss_url=src["rss_url"]
            ))

    db.commit()
    db.close()

if __name__ == "__main__":
    seed()