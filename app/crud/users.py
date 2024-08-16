from sqlalchemy.orm import Session
from passlib.context import CryptContext
import logging

from ..schemas.users import UserCreate, UserResponse, UserInDB
from ..models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data from the request.

    Returns:
        User: The created User object.
    """
    logger.info(f"Creating user {user.username}")
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Refresh to get the full user object from the DB, including the ID
        logger.info(f"User {user.username} created successfully")
        db_user = UserResponse(message="User created successfully", data= UserInDB(email=db_user.email, id=db_user.user_id, username=db_user.username, password=db_user.hashed_password))
        return db_user
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating user {user.username}: {str(e)}")
        raise

def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Fetch a user by their username.

    Args:
        db (Session): The database session.
        username (str): The username to search for.

    Returns:
        User | None: The User object if found, otherwise None.
    """
    logger.info(f"Fetching user with username {username}")
    data = db.query(User).filter(User.username == username).first()
    if not data:
        logger.warning(f"User with username {username} not found")
        return None

    logger.info(f"Found user: {data.username}")
    return data
