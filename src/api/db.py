from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os



# DATABASE_URL = "postgresql://postgres:root1234@localhost:5432/it_assistant"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"
)
engine = create_engine(DATABASE_URL,connect_args={"options": "-c client_encoding=utf8"})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()