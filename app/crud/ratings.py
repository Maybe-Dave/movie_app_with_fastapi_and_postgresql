import logging
from uuid import UUID, uuid4
from fastapi import HTTPException

from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.ratings import Rating
from ..models.movies import Movie
from ..schemas.ratings import RatingCreate, RatingResponse
from decimal import Decimal

logger = logging.getLogger(__name__)

def get_ratings(db: Session, movie_id: int) -> RatingResponse:
    logger.info(f"Fetching ratings for movie {movie_id}")
    # check if movie exists
    movie_exists = db.query(Movie).filter(Movie.movie_id == movie_id).scalar()
    if not movie_exists:
        logger.error(f"Movie with id {movie_id} does not exist")
        raise HTTPException(status_code=404, detail=f"Movie with id {movie_id} does not exist")

    ratings: List[Rating] = db.query(Rating).filter(Rating.movie_id == movie_id).all()
    
    if not ratings:
        logger.error(f"No ratings found for movie {movie_id}")
        raise HTTPException(status_code=404, detail=f"No ratings found for movie with id {movie_id}")

    logger.info(f"Calculating average rating for movie {movie_id}")
    average_rating = db.query(func.avg(Rating.rating)).filter(Rating.movie_id == movie_id).scalar()
    average_rating = round(average_rating, 2) if average_rating else Decimal(0.0)

    movie_title = db.query(Movie.title).filter(Movie.movie_id == movie_id).scalar()
    
    result = RatingResponse(
        movie_id=movie_id,
        movie_title=movie_title,
        average_rating=average_rating
    )
    logger.info(f"Returning ratings for movie {movie_id}")
    return result

def set_movie_rating(db: Session, rating_data: RatingCreate, user_id: UUID) -> RatingResponse:
    # Check if movie exists
    movie_title = db.query(Movie.title).filter(Movie.movie_id == rating_data.movie_id).scalar()

    if not movie_title:
        logger.error(f"Movie with id {rating_data.movie_id} does not exist")
        raise HTTPException(status_code=404, detail=f"Movie with id {rating_data.movie_id} does not exist")

    logger.info(f"Setting rating for movie {rating_data.movie_id} by user {user_id}")
    existing_rating = db.query(Rating).filter(
        Rating.movie_id == rating_data.movie_id,
        Rating.user_id == user_id
    ).first()
    
    if existing_rating:
        logger.info(f"Rating already exists for movie {rating_data.movie_id} by user {user_id}")
        existing_rating.rating = rating_data.rating
    else:
        new_rating = Rating(
            id=uuid4(),
            movie_id=rating_data.movie_id,
            user_id=user_id,
            rating=rating_data.rating
        )
        db.add(new_rating)
    
    try:
        db.commit()
    except IntegrityError as e:
        logger.error(f"IntegrityError: Failed to set rating for movie {rating_data.movie_id} by user {user_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to set rating due to integrity constraints.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred while setting the rating.")
    
    updated_rating = db.query(Rating).filter(
        Rating.movie_id == rating_data.movie_id,
        Rating.user_id == user_id
    ).first()

    logger.info(f"Rating set for movie {rating_data.movie_id} by user {user_id}") 
    result = RatingResponse(
        movie_id=updated_rating.movie_id,
        movie_title=movie_title,
        average_rating=get_ratings(db, updated_rating.movie_id).average_rating
    )
    return result
