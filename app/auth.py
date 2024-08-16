import os
import logging
from datetime import timedelta, timezone, datetime
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from calendar import timegm  

from .crud.users import get_user_by_username
from .database import get_db
from .models.users import User

logger = logging.getLogger(__name__)

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    :param plain_password: The plaintext password to verify.
    :param hashed_password: The hashed password to verify against.
    :return: True if the password matches, False otherwise.
    """
    logger.info("Verifying password")
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """
    Authenticate the user by their username and password.

    :param db: The database session.
    :param username: The username to authenticate.
    :param password: The plaintext password to verify.
    :return: The authenticated user or None if authentication fails.
    """
    logger.info("Authenticating user")
    user = get_user_by_username(db, username)
    if not user:
        logger.warning(f"Authentication failed: User {username} not found")
        return None
    if not verify_password(password, user.hashed_password):
        logger.warning(f"Authentication failed: Incorrect password for user {username}")
        return None
    
    logger.info(f"User {username} authenticated successfully")
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    :param data: The data to include in the token payload.
    :param expires_delta: Optional timedelta for token expiration.
    :return: A signed JWT token.
    """    
    logger.info("Creating access token")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Use timegm to convert the datetime to a Unix timestamp
    expire_timestamp = timegm(expire.utctimetuple())
    to_encode.update({"exp": expire_timestamp})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("Access token created successfully")
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the current user based on the provided JWT token.

    :param token: The JWT token from the Authorization header.
    :param db: The database session.
    :return: The authenticated user.
    :raises HTTPException: If the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    logger.info("Retrieving current user from token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            logger.error("Token does not contain a username")
            raise credentials_exception
    except JWTError as e:
        logger.error(f"Error decoding token: {str(e)}")
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        logger.error(f"User not found: {username}")
        raise credentials_exception

    logger.info(f"Current user {username} retrieved successfully")
    return user
