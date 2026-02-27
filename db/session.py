from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./todo.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # cần cho SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)