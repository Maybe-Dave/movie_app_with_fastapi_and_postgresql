import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth import authenticate_user, create_access_token
from ..schemas.users import UserCreate, UserResponse
from ..crud.users import create_user, get_user_by_username
from ..database import get_db

logger = logging.getLogger(__name__)

users_router = APIRouter()

@users_router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (UserCreate): The user data from the request.
        db (Session): The database session.

    Returns:
        UserResponse: The created user data wrapped in a response message.
    """
    logger.info(f"Creating user with username={user.username}")
    db_user = get_user_by_username(db, user.username)
    if db_user:
        logger.warning(f"User with username={user.username} already exists")
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = create_user(db, user)
    logger.info(f"User with username={user.username} created successfully")
    return new_user

@users_router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login credentials (username and password).
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    logger.info(f"Authenticating user with username={form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning("Incorrect username or password")
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or password", 
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": user.username})
    logger.info("User authenticated successfully")
    return {"access_token": access_token, "token_type": "bearer"}
