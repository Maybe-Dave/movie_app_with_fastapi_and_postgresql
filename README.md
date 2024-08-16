
# Project Title
FastAPI AND POSTGRESQL MOVIE APP
## Description
This project is a FastAPI-based web application that provides endpoints for managing movies and their ratings. It includes user authentication, movie creation, rating management, and more.

## Dependencies
- Python 3.9+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- Pytest (for testing)
## Features
- **User Authentication**: Users can sign up, log in, and obtain JWT tokens for accessing protected routes.
- **Movie Management**: Authenticated users can create, update, and view movies.
- **Rating System**: Users can rate movies and view aggregated ratings.
- **Comment System**: Users can add comments to movies, including nested comments.
## Installation
1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/fastapi-movie-ratings.git
    cd fastapi-movie-ratings
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following environment variables:

    ```dotenv
    SECRET_KEY=your_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DATABASE_URL=sqlite:///./test.db
    ```

5. **Apply database migrations:**

    ```bash
    alembic upgrade head
    ```

6. **Run the application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.
## Installation
1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/fastapi-movie-ratings.git
    cd fastapi-movie-ratings
    ```

2. **Create a virtual environment and activate it:**

    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following environment variables:

    ```dotenv
    SECRET_KEY=your_secret_key_here
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DATABASE_URL=sqlite:///./test.db
    ```

5. **Apply database migrations:**

    ```bash
    alembic upgrade head
    ```

6. **Run the application:**

    ```bash
    uvicorn app.main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.
## Endpoints
### Auth Endpoints

- `POST /signup` - Create a new user account.
- `POST /login` - Authenticate and get a JWT token.

### Movie Endpoints

- `POST /movies/` - Create a new movie.
- `GET /movies/{movie_id}` - Get details of a movie by ID.
- `PUT /movies/{movie_id}` - Update an existing movie.
- `DELETE /movies/{movie_id}` - Delete a movie.

### Rating Endpoints

- `POST /ratings/` - Rate a movie.
- `GET /ratings/{movie_id}` - Get ratings for a movie.

### Comment Endpoints

- `POST /comments/` - Add a comment to a movie.
- `GET /comments/{movie_id}` - View comments for a movie.
- `POST /comments/reply/{parent_id}` - Add comment to a comment
## Running Tests
To run the tests, use the following command:

```bash
pytest
## Logging
Logging
Logging is set up throughout the application, capturing key actions and errors. Logs are printed to the console, and can be directed to a file or other logging handlers by adjusting the logging configuration in the code.
## Contributing
Contributing
Feel free to contribute to this project by submitting issues or pull requests. Make sure to follow the project's code style and testing practices.
## Author
David Dickson
## License
This project is licensed under the David License - see the LICENSE.md file for details