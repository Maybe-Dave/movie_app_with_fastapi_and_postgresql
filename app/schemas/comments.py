from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID

class CommentBase(BaseModel):
    """
    Base schema for Comment. This schema includes common fields shared by multiple
    Comment-related schemas.
    
    Attributes:
        content (str): The content of the comment. This is a required field and contains the main text of the comment.
        movie_id (int): The ID of the movie that the comment is associated with. This is a required field.
    """
    content: str
    movie_id: int

class CommentCreate(CommentBase):
    """
    Schema for creating a new Comment. Inherits from CommentBase and is used to validate
    data when creating a new comment.
    
    Inherits:
        CommentBase: The base schema for a comment, containing content and movie_id.
    """
    pass

class CommentInDB(CommentBase):
    """
    Schema representing a Comment as stored in the database. Inherits from CommentBase 
    and includes additional fields such as id, user_id, parent_id, and replies, which represent 
    the comment's unique identifier, the user who created it, the parent comment for nested 
    comments, and a list of replies, respectively.
    
    Attributes:
        id (UUID): The unique identifier for the comment. This is a required field.
        user_id (UUID): The unique identifier for the user who created the comment. This is a required field.
        parent_id (Optional[UUID]): The ID of the parent comment, if this comment is a reply. This field is optional.
        replies (List["CommentInDB"]): A list of replies to this comment. Defaults to an empty list.
    
    Inherits:
        CommentBase: The base schema for a comment, containing content and movie_id.
    """
    id: UUID
    user_id: UUID
    parent_id: Optional[UUID] = None
    replies: List["CommentInDB"] = []

    model_config = ConfigDict(from_attributes=True, orm_mode=True)


class CommentReply(CommentBase):
    """
    Schema for creating a reply to a Comment. Inherits from CommentBase and includes
    the parent_id field to associate the reply with a parent comment.
    
    Attributes:
        parent_id (UUID): The ID of the parent comment to which this reply is associated. This is a required field.
    
    Inherits:
        CommentBase: The base schema for a comment, containing content and movie_id.
    """
    parent_id: UUID
    pass
