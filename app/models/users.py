from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from ..database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String(30), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    comments = relationship("Comment", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    movies = relationship("Movie", back_populates="creator")
