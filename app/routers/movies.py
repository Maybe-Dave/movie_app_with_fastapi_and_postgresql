import logging

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..schemas.movies import MovieCreate, MovieResponse, MovieUpdate, MovieInDB
from ..database import get_db
from ..crud.movies import get_movies, get_movie_id, add_movie, get_movie_title, update_movie_by_id, delete_by_id
from ..auth import get_current_user
from ..models.users import User

logger = logging.getLogger(__name__)

movies_router = APIRouter()

@movies_router.get("/", response_model=MovieResponse)
async def get_all_movies(db: Session = Depends(get_db)):
    """
    Retrieve all movies from the database.
    """
    logger.info("Fetching all movies")
    db_movies = get_movies(db)
    logger.info(f"Found {len(db_movies.data)} movies")
    return db_movies

@movies_router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific movie by its ID.
    """
    logger.info(f"Fetching movie with id={movie_id}")
    db_movie = get_movie_id(db, movie_id)
    logger.info(f"Found movie: {db_movie.data.title}")
    return db_movie

@movies_router.get("/by_title/{title}", response_model=MovieResponse)
async def get_movie_by_title(title: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific movie by its title.
    """
    logger.info(f"Fetching movie with title={title}")
    db_movie = get_movie_title(db, title)
    logger.info(f"Found movie: {db_movie.data.title}")
    return db_movie

@movies_router.post("/", response_model=MovieResponse)
async def create_movie(payload: MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new movie in the database.
    """
    logger.info(f"Adding movie with title={payload.title}")
    movie = add_movie(db, payload, current_user.user_id)
    logger.info(f"Added movie with title={movie.data.title}")
    return movie

@movies_router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(movie_id: int, payload: MovieUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Update an existing movie in the database.
    """
    logger.info(f"Updating movie with id={movie_id}")
    movie = update_movie_by_id(db=db, movie=payload, movie_id=movie_id, user_id=current_user.user_id)
    logger.info(f"Updated movie with id={movie_id}")
    return movie

@movies_router.delete("/{movie_id}", response_model=MovieResponse)
async def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: User= Depends(get_current_user)):
    """
    Delete a movie from the database.
    """
    logger.info(f"Deleting movie with id={movie_id}")
    movie = delete_by_id(db, movie_id, current_user.user_id)
    logger.info(f"Deleted movie with id={movie_id}")
    return movie
