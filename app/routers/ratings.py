from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import logging
from pydantic import conint

from ..database import get_db
from ..auth import get_current_user
from ..crud.ratings import get_ratings, set_movie_rating
from ..schemas.ratings import RatingCreate, RatingResponse
from ..schemas.users import UserInDB
from ..models.users import User

logger = logging.getLogger(__name__)

ratings_router = APIRouter()

@ratings_router.get("/", response_model=RatingResponse)
async def get_movie_ratings(movie_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the aggregate rating for a specific movie.

    Parameters:
        - movie_id (int): The ID of the movie to retrieve ratings for.
        - db (Session): The database session.

    Returns:
        - RatingResponse: The aggregate rating for the movie.
    """
    logger.info(f"Fetching rating for movie with id={movie_id}")
    rating = get_ratings(db, movie_id)
    logger.info(f"Returning rating for movie with id={movie_id}")
    return rating

@ratings_router.post("/", response_model=RatingResponse)
async def rate_movie(rating: RatingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Add a new rating for a specific movie.

    Parameters:
        - rating (RatingCreate): The data needed to create the rating.
        - db (Session): The database session.
        - current_user (User): The currently authenticated user.

    Returns:
        - RatingResponse: The newly created rating.
    """
    logger.info(f"Adding rating for movie with id={rating.movie_id}")
    db_rating = set_movie_rating(db, rating, current_user.user_id)
    logger.info(f"Added rating for movie with id={rating.movie_id}")
    return db_rating
