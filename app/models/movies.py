from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base

class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    release_date = Column(Date, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    # Relationships
    creator = relationship("User", back_populates="movies")
    ratings = relationship("Rating", back_populates="movie")
    comments = relationship("Comment", back_populates="movie")
