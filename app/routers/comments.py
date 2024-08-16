from fastapi import APIRouter, Depends
from typing import List
import logging

from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.comments import CommentCreate, CommentInDB, CommentReply
from ..crud.comments import add_comment, get_comments_by_movie, add_nested_comment
from ..models.users import User
from ..auth import get_current_user

logger = logging.getLogger(__name__)

comments_router = APIRouter()

@comments_router.post("/", response_model=CommentInDB)
async def create_comment(payload: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new comment for a movie.

    Parameters:
        - payload (CommentCreate): The data needed to create the comment.
        - db (Session): The database session.
        - current_user (User): The currently authenticated user.

    Returns:
        - CommentInDB: The newly created comment.
    """
    logger.info(f"Creating comment for movie_id={payload.movie_id} by user_id={current_user.user_id}")
    comment = add_comment(db, payload, current_user.user_id)
    logger.info(f"Comment created with id={comment.id}")
    return comment

@comments_router.get("/{movie_id}", response_model=List[CommentInDB])
async def get_comments(movie_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all comments for a specific movie.

    Parameters:
        - movie_id (int): The ID of the movie.
        - db (Session): The database session.

    Returns:
        - List[CommentInDB]: A list of all comments for the movie, including nested replies.
    """
    logger.info(f"Fetching comments for movie_id={movie_id}")
    comments = get_comments_by_movie(db, movie_id)
    logger.info(f"Found {len(comments)} comments for movie_id={movie_id}")
    return comments

@comments_router.post("/reply/{parent_id}", response_model=CommentInDB)
async def reply_comment(payload: CommentReply, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Reply to an existing comment.

    Parameters:
        - payload (CommentReply): The data needed to create the reply.
        - db (Session): The database session.
        - current_user (User): The currently authenticated user.

    Returns:
        - CommentInDB: The newly created reply.
    """
    logger.info(f"Creating reply for the comment with id={payload.parent_id} by user_id={current_user.user_id}")
    comment = add_nested_comment(db, payload=payload, user_id=current_user.user_id)
    logger.info(f"Reply created with id={comment.id}")
    return comment
