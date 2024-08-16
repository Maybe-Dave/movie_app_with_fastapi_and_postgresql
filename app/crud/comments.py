from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
import logging
from fastapi import HTTPException

from ..models.comments import Comment
from ..schemas.comments import CommentCreate, CommentInDB, CommentReply

logger = logging.getLogger(__name__)

def add_comment(db: Session, comment: CommentCreate, user_id: UUID) -> Comment:
    logger.info(f"Adding comment for movie {comment.movie_id} by user {user_id}")
    db_comment = Comment(
        content=comment.content,
        movie_id=comment.movie_id,
        user_id=user_id,
        parent_id=None  # Not a reply
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    logger.info(f"Comment added with id {db_comment.id}")
    return db_comment


def get_comments_by_movie(db: Session, movie_id: int) -> List[CommentInDB]:
    logger.info(f"Fetching comments for movie {movie_id}")
    top_level_comments = db.query(Comment).filter(Comment.movie_id == movie_id, Comment.parent_id.is_(None)).all()

    if not top_level_comments:
        logger.error(f"No comments found for movie {movie_id}")
        raise HTTPException(status_code=404, detail="No comments found for this movie")

    def fetch_replies(comment: Comment) -> CommentInDB:
        replies = db.query(Comment).filter(Comment.parent_id == comment.id).all()
        comment_in_db = CommentInDB(
            id=comment.id,
            user_id=comment.user_id,
            content=comment.content,
            movie_id=comment.movie_id,
            parent_id=comment.parent_id,
            replies=[fetch_replies(reply) for reply in replies]
        )
        return comment_in_db

    all_comments = [fetch_replies(comment) for comment in top_level_comments]

    logger.info(f"Returning comments for movie {movie_id}")

    return all_comments

def add_nested_comment(db: Session, payload: CommentReply, user_id: UUID) -> Comment:
    logger.info(f"Adding reply comment for movie {payload.movie_id} by user {user_id}")
    reply_comment = Comment(
        content=payload.content,
        movie_id=payload.movie_id,
        user_id=user_id,
        parent_id=payload.parent_id
    )
    db.add(reply_comment)
    db.commit()
    db.refresh(reply_comment)
    logger.info(f"Reply comment added with id {reply_comment.id}")
    return reply_comment
