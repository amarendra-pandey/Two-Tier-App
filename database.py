from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

db_url = DATABASE_URL#"postgresql://postgres:password@localhost:5432/fastapi_db"

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal();

    try:
        yield db
    finally:
        db.close()