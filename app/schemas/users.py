from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    """
    Base schema for User. This schema includes common fields 
    shared by multiple User-related schemas.
    
    Attributes:
        username (str): The username of the user. It must be unique and is a required field.
        email (EmailStr): The email address of the user. It must follow standard email formatting.
    """
    username: str
    email: str

class UserCreate(UserBase):
    """
    Schema for creating a new User. Inherits from UserBase and adds a password field.
    
    Attributes:
        password (str): The password for the user. This is required during user registration.
    """
    password: str

class UserInDB(UserBase):
    """
    Schema representing a User as stored in the database. Inherits from UserBase 
    and includes an id field representing the user's unique identifier.
    
    Attributes:
        id (UUID): The unique identifier for the user. This is a UUID that uniquely 
        identifies each user in the database.
    """
    id: UUID

    model_config = ConfigDict(from_attributes=True, orm_mode=True)
    """
    Config settings for Pydantic model:
    - from_attributes: Enables compatibility with SQLAlchemy ORM models.
    """

class UserResponse(BaseModel):
    """
    Schema representing the response data for a User. This schema includes a message 
    and the user data returned after a successful operation.
    
    Attributes:
        message (str): A message indicating the result of the operation.
        data (UserInDB): The user data returned after a successful operation.
    """
    message: str
    data: UserInDB
