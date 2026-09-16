from sqlalchemy import create_engine, URL
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import load_data_directory

DATABASE_URL = URL.create('sqlite', database=str(load_data_directory() / 'career_assistant.db'))

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
