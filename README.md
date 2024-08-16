# FastAPI and PostgreSQL Movie App

## Description

This project is a FastAPI-based web application that provides a comprehensive platform for managing movies, ratings, and comments. It includes user authentication with JWT, a rating system, a comment system with nested replies, and the ability to perform CRUD operations on movies. The application is deployed on Render and includes a mechanism to keep the service active using a cron job.

## Features

- **User Authentication**: Users can sign up, log in, and obtain JWT tokens for accessing protected routes.
- **Movie Management**: Authenticated users can create, update, view, and delete movies.
- **Rating System**: Users can rate movies and view aggregated ratings.
- **Comment System**: Users can add comments to movies, including nested replies.
- **Persistent Uptime**: The application includes a cron job to periodically ping the app to prevent deactivation on Render.
- **Logging**: Comprehensive logging is implemented across the application to capture key actions and errors.

## Dependencies

- Python 3.9+
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn
- PostgreSQL
- Pytest (for testing)

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
    DATABASE_URL=postgresql://user:password@localhost/dbname
    ```

5. **Apply database migrations:**

    ```bash
    alembic upgrade head
    ```

6. **Create the `ping_app.sh` script:**

    Place the `ping_app.sh` script in the root directory:

    ```bash
    #!/bin/bash

    # Replace with your FastAPI app's URL
    APP_URL="https://your-app-url.onrender.com/"

    # Send a GET request to the FastAPI app
    curl -I $APP_URL
    ```

    Make the script executable:

    ```bash
    chmod +x ping_app.sh
    ```

7. **Add the `render.yaml` file:**

    Create a `render.yaml` file in the root directory with the following content to set up a cron job:

    ```yaml
    services:
      - type: web
        name: fastapi-movie-app
        env: python
        plan: free
        buildCommand: pip install -r requirements.txt
        startCommand: uvicorn app.main:app --host 0.0.0.0 --port 8000

    jobs:
      - name: ping-app
        env: python
        plan: free
        cron: "*/5 * * * *"
        command: ./ping_app.sh
    ```

8. **Run the application:**

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
- `GET /movies/` - Get details of all movies.
- `GET /movies/{movie_id}` - Get details of a movie by ID.
- `GET /movies/{title}` - Get details of a movie by title.
- `PUT /movies/{movie_id}` - Update an existing movie.
- `DELETE /movies/{movie_id}` - Delete a movie.

### Rating Endpoints

- `POST /ratings/` - Rate a movie.
- `GET /ratings/{movie_id}` - Get ratings for a movie.

### Comment Endpoints

- `POST /comments/` - Add a comment to a movie.
- `GET /comments/{movie_id}` - View comments for a movie.
- `POST /comments/reply/{parent_id}` - Add a reply to a comment.

## Running Tests

To run the tests, use the following command:

```bash
pytest

## Logging
Logging
Logging is set up throughout the application, capturing key actions and errors. Logs are printed to the console, and can be directed to a file or other logging handlers by adjusting the logging configuration in the code.
## Contribution
Feel free to contribute to this project by submitting issues or pull requests. Make sure to follow the project's code style and testing practices.
## Deployment
The application is deployed on Render. To keep the service active, a cron job is set up via the render.yaml file, which pings the application every 5 minutes using the ping_app.sh script.
## Author
David Dickson
## License
This project is licensed under the David License - see the LICENSE.md file for details

```
This `README.md` file is now formatted correctly and includes all the necessary information about your FastAPI and PostgreSQL Movie App.
```
