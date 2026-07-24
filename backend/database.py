import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    result = db.execute(text("SELECT @@VERSION AS version, DB_NAME() AS db_name"))
    row = result.fetchone()
    # Ensure row is accessed properly whether it acts as a tuple or dict
    version = row[0] if row else "Unknown"
    db_name = row[1] if row else "Unknown"
    print(f"Database connected: {db_name} (Version: {version})")
    try:
        yield db
    finally:
        db.close()
