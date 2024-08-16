from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from decimal import Decimal

class RatingBase(BaseModel):
    """
    Base schema for Rating. This schema includes common fields shared by multiple
    Rating-related schemas.
    
    Attributes:
        movie_id (int): The ID of the movie that the rating is associated with. This is a required field.
    """
    movie_id: int

class RatingCreate(RatingBase):
    """
    Schema for creating a new Rating. Inherits from RatingBase and adds a rating field.
    Used to validate data when a user submits a new rating for a movie.
    
    Attributes:
        rating (int): The rating score given by the user, which must be between 1 and 5.
    
    Inherits:
        RatingBase: The base schema for a rating, containing the movie_id.
    """
    rating: int = Field(..., ge=1, le=5)

    model_config = ConfigDict(from_attributes=True)

class RatingInDB(RatingBase):
    """
    Schema representing a Rating as stored in the database. Inherits from RatingBase
    and includes additional fields such as id and user_id, which represent the rating's
    unique identifier and the user who created it, respectively.
    
    Attributes:
        id (UUID): The unique identifier for the rating. This is a required field.
        user_id (UUID): The unique identifier for the user who created the rating. This is a required field.
    
    Inherits:
        RatingBase: The base schema for a rating, containing the movie_id.
    """
    id: UUID
    user_id: UUID
    rating: int = Field(..., ge=1, le=5)
    
    model_config = ConfigDict(from_attributes=True, orm_mode=True)

class RatingResponse(BaseModel):
    """
    Schema representing the response for a Rating. This schema includes the movie_id,
    the average rating for the movie, and the movie title.
    
    Attributes:
        movie_id (int): The ID of the movie.
        movie_title (str): The title of the movie.
        average_rating (Decimal): The average rating for the movie.
    """
    movie_id: int
    movie_title: str
    average_rating: float

    
