from pydantic import BaseModel, ConfigDict
from typing import List, Union, Optional
from uuid import UUID
from datetime import date

class MovieBase(BaseModel):
    """
    Base schema for Movie. This schema includes common fields shared by multiple
    Movie-related schemas.
    
    Attributes:
        title (str): The title of the movie. This is a required field and should be a descriptive name.
        description (Optional[str]): A brief description of the movie. This field is optional.
        release_date (date): The release date of the movie. It is required and should follow the datetime format.
    """
    title: str
    description: Optional[str] = None
    release_date: date

class MovieCreate(MovieBase):
    """
    Schema for creating a new Movie. Inherits from MovieBase and is used to validate
    data when creating a new movie entry.
    """
    pass

class MovieUpdate(MovieBase):
    """
    Schema for updating an existing Movie. Inherits from MovieBase and is used to validate
    data when updating a movie entry.
    """
    pass

class MovieInDB(MovieBase):
    """
    Schema representing a Movie as stored in the database. Inherits from MovieCreate 
    and includes an id field and user_id field representing the movie's unique identifier 
    and the user who created it, respectively.
    
    Attributes:
        id (int): The unique identifier for the movie in the database. It is a required field.
        user_id (UUID): The unique identifier for the user who created the movie. This is a UUID.
    """
    id: int
    user_id: UUID

    model_config = ConfigDict(from_attributes=True, orm_mode=True)

class MovieResponse(BaseModel):
    """
    Schema for a movie response. Includes a message field to indicate the status of the operation.
    
    Attributes:
        message (str): A message indicating the status of the operation.
        data (Union[MovieInDB, List[MovieInDB]]): The movie data, either as a single item or a list.
    """
    message: str
    data: Union[MovieInDB, List[MovieInDB]]
