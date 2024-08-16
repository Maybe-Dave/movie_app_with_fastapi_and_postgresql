from sqlalchemy import Column, ForeignKey, Text, UUID, Integer
from sqlalchemy.orm import relationship
import uuid

from ..database import Base

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('comments.id'), nullable=True)
    
    # Relationships
    movie = relationship("Movie", back_populates="comments")
    user = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")
