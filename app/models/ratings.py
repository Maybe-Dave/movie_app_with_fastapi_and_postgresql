from sqlalchemy import Column, ForeignKey, Integer, UUID, CheckConstraint
from sqlalchemy.orm import relationship
import uuid

from ..database import Base

class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    rating = Column(Integer, nullable=False,index=True)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )

    # Relationships
    movie = relationship("Movie", back_populates="ratings")
    user = relationship("User", back_populates="ratings")
