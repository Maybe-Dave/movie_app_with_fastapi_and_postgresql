import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager


from .database import Base, engine
from .routers.comments import comments_router
from .routers.ratings import ratings_router
from .routers.users import users_router
from .routers.movies import movies_router

# Create all the database tables
Base.metadata.create_all(bind=engine)

# Setup basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Log format
)

logger = logging.getLogger(__name__)  # Create a logger for this module

# Context manager for application startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")    
    yield 
    logger.info("Application shutdown")


# Initialize the FastAPI app with a lifespan context manager
app = FastAPI(lifespan=lifespan)


# Include routers for different modules
app.include_router(router=users_router,tags=["USER"])
app.include_router(router=ratings_router,prefix="/ratings",tags=["RATING"])
app.include_router(router=comments_router,prefix="/comments",tags=["COMMENT"])
app.include_router(router=movies_router,prefix="/movies",tags=["MOVIE"])



    
@app.get("/")
async def root():
    return {"message": "Welcome to the Movie Rating App"}
