from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi import HTTPException
import logging

from ..models.movies import Movie
from ..schemas.movies import MovieCreate, MovieInDB, MovieUpdate, MovieResponse

logger = logging.getLogger(__name__)


def get_movies(db: Session) -> MovieResponse:
    logger.info("Fetching all movies")
    db_movies = db.query(Movie).offset(0).limit(10).all()
    
    if not db_movies:
        logger.error("No movies found")
        raise HTTPException(status_code=404, detail="No movies found")
    
    logger.info(f"Found {len(db_movies)} movies")
    
    # Manually map each SQLAlchemy model instance to a Pydantic model instance
    movies = [
        MovieInDB(
            id=movie.movie_id,
            title=movie.title,
            description=movie.description,
            release_date=movie.release_date,
            user_id=movie.user_id,
        )
        for movie in db_movies
    ]
    
    response = MovieResponse(message="Movies retrieved successfully", data=movies)
    return response

def get_movie_id(db: Session, movie_id: int) -> MovieResponse:
    logger.info(f"Fetching movie with id={movie_id}")
    data = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not data:
        logger.warning(f"Movie with id={movie_id} not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    logger.info(f"Found movie: {data.title}")
    data = MovieResponse(message="Movie retrieved successfully", data=MovieInDB(title=data.title, description=data.description, release_date=data.release_date, id=data.movie_id, user_id=data.user_id))
    return data

def get_movie_title(db: Session, title: str) -> MovieResponse:
    logger.info(f"Fetching movie with title={title}")
    data = db.query(Movie).filter(Movie.title == title).first()
    if not data:
        logger.warning(f"Movie with title={title} not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    logger.info(f"Found movie: {data.title}")
    data = MovieResponse(message="Movie retrieved successfully", data=MovieInDB(title=data.title, description=data.description, release_date=data.release_date, id=data.movie_id, user_id=data.user_id))
    return data

def add_movie(db: Session, movie: MovieCreate, user_id: UUID) -> MovieResponse:
    logger.info(f"Adding movie by user with id={user_id}")

    if movie.title == "string" or movie.title.strip() == "":
        logger.error("Title is required")
        raise HTTPException(status_code=400, detail="Title is required")
    if movie.description == "string" or movie.description.strip() == "":
        logger.error("Description is required")
        raise HTTPException(status_code=400, detail="Description is required")

    db_movie = Movie(
        title=movie.title,
        description=movie.description,
        release_date=movie.release_date,
        user_id=user_id
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    logger.info(f"Added movie with id={db_movie.user_id}")
    db_movie = MovieResponse(message="Movie added successfully", data=MovieInDB(title=db_movie.title, description=db_movie.description, release_date=db_movie.release_date, id=db_movie.movie_id, user_id=db_movie.user_id))
    return db_movie

def update_movie_by_id(db: Session, movie_id: int, movie: MovieUpdate, user_id: UUID) -> MovieResponse:
    logger.info(f"Updating movie with id={movie_id}")
    db_movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    
    if db_movie is None:
        logger.warning(f"Movie with id={movie_id} not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if db_movie.user_id != user_id:
        logger.warning(f"User with id={user_id} is not authorized to update")
        raise HTTPException(status_code=403, detail="You are not authorized to update")
    
    if movie.title and movie.title != "string" and movie.title.strip():
        db_movie.title = movie.title
    if movie.description and movie.description != "string" and movie.description.strip():
        db_movie.description = movie.description

    db.commit()
    db.refresh(db_movie)
    logger.info(f"Updated movie with id={movie_id}")
    db_movie = MovieResponse(message="Movie updated successfully", data=MovieInDB(title=db_movie.title, description=db_movie.description, release_date=db_movie.release_date, id=db_movie.movie_id, user_id=db_movie.user_id))
    return db_movie

def delete_by_id(db: Session, movie_id: int, user_id: UUID) -> MovieResponse:
    logger.info(f"Deleting movie with id={movie_id}")
    db_movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()

    if db_movie is None:
        logger.warning(f"Movie with id={movie_id} not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if db_movie.user_id != user_id:
        logger.warning(f"User with id={user_id} is not authorized to delete")
        raise HTTPException(status_code=403, detail="You are not authorized to delete")
    
    data=MovieInDB(title=db_movie.title, description=db_movie.description, release_date=db_movie.release_date, id=db_movie.movie_id, user_id=db_movie.user_id)
    
    db.delete(db_movie)
    db.commit()
    logger.info(f"Deleted movie with id={movie_id}")
    db_movie = MovieResponse(message="Movie deleted successfully", data=data)
    return db_movie
