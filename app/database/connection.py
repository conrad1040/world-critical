from sqlalchemy import create_engine

from app.database.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)


def connect():
    with engine.connect() as connection:
        print("✅ Connected to PostgreSQL!")