from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from logger import get_logger

DATABASE_URL = "postgresql://orderuser:orderpass@postgres:5432/ecommerce"

logger = get_logger()

Base = declarative_base()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        logger.info("Database session opened")
        yield db
    finally:
        db.close()
        logger.info("Database session closed")

