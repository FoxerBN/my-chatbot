# src/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import DB_URL

Base = declarative_base()

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    import src.model.chat_model
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()