import os
from dotenv import load_dotenv
from fastapi import HTTPException

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Load the database URL from the environment variable
SQLALCHEMY_DATABASE_URL = os.environ.get('DB_URL')

if not SQLALCHEMY_DATABASE_URL:
    raise HTTPException(status_code=500, detail="Database URL not found")

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative class definitions
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
