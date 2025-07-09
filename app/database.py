from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG  # Shows SQL queries in console when DEBUG=True
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for all models
Base = declarative_base()

# Dependency to get database session
def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()