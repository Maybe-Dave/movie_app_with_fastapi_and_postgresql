import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app

from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
#=================================================== Test Cases=========================================================================
# ========================
# Users endpoints
# ========================
@pytest.mark.parametrize("username, password, email", [("testuser", "testpassword", "Test_email@gmail.com")])
def test_signup(client, setup_database,username, password, email):
    response = client.post("/signup", json={"username": username, "password": password, "email": email})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["username"] == username

    # Signup with the same username
    response = client.post("/signup", json={"username": username, "password": password, "email": email})
    assert response.status_code == 400

    # create another user
    response = client.post("/signup", json={"username": "testuser2", "password": "testpassword2", "email": "Test email 2"})
    assert response.status_code == 200


@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_login(client, setup_database, username, password):
    # Login with the created user
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Login with invalid credentials
    response = client.post("/login", data={"username": username, "password": "wrongpassword"})
    assert response.status_code == 400

# # # ========================
# # # Mvie Endpoints
# # # ========================
    
# Test before Movie creation
def test_get_movie(client, setup_database):


    # Get books
    response = client.get("/movies/")
    assert response.status_code == 404

    data = response.json()
    assert data == {"detail": "No movies found"}
  
    

@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_create_movies(client, setup_database, username, password):

    # Login with the created user
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Create a movie
    response = client.post("/movies/", 
                           json={"title": "Test Book", "description": "Test Description", "release_date": "2024-08-15"},
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie added successfully"
    assert data["data"]["title"] == "Test Book"
    assert data["data"]["description"] == "Test Description"

#     # Create another movie
    response = client.post("/movies/", 
                           json={"title": "Test Book 2", "description": "Test Description 2", "release_date": "2024-08-15"},
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie added successfully"
    assert data["data"]["title"] == "Test Book 2"
    assert data["data"]["description"] == "Test Description 2"

    # Create a moviw by another user
    response = client.post("/login", data={"username": "testuser2", "password": "testpassword2"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    response = client.post("/movies/",
                            json={"title": "Test Book 3", "description": "Test Description 3", "release_date": "2024-08-15"},
                            headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie added successfully"
    assert data["data"]["title"] == "Test Book 3"
    assert data["data"]["description"] == "Test Description 3"
    assert data["data"]["id"] == 3

# # Test After book creation
def test_get_movies(client, setup_database):
    
    # Get Movie
    response = client.get("/movies/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 3

    # Get Movie by id
    response = client.get("/movies/1")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == 1
    assert data["data"]["title"] == "Test Book"
    assert data["data"]["description"] == "Test Description"

    # Get Movie by title
    response = client.get("/movies/by_title/Test Book 2")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == 2
    assert data["data"]["title"] == "Test Book 2"
    assert data["data"]["description"] == "Test Description 2"


    # Get Movie by invalid id
    response = client.get("/movies/4")
    assert response.status_code == 404

    # Get Movie by invalid title
    response = client.get("/movies/by_title/Invalid Title")
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Movie not found"}

# Test Update Movie
@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_update_movie(client, setup_database,username, password):
    # Login with the user 1
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Update with default payload
    response = client.put("/movies/1", 
                          json={"title": "string", "description": "string","release_date": "2024-08-15"},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie updated successfully"
    assert data["data"]["title"] == "Test Book"
    assert data["data"]["description"] == "Test Description"

    # Update Movie
    response = client.put("/movies/1", 
                          json={"title": "Updated Book", "description": "Updated Description","release_date": "2024-08-15"},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie updated successfully"
    assert data["data"]["title"] == "Updated Book"
    assert data["data"]["description"] == "Updated Description"

    # Update Movie with invalid id
    response = client.put("/movies/4", 
                          json={"title": "Updated Book", "description": "Updated Description","release_date": "2024-08-15"},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Movie not found"}

    # Update Movie with invalid user
    response = client.put("/movies/3", 
                          json={"title": "Updated Book", "description": "Updated Description","release_date": "2024-08-15"},
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    data = response.json()
    assert data == {"detail": "You are not authorized to update"}

# Test Delete Movie
@pytest.mark.parametrize("username, password", [("testuser", "testpassword")])
def test_delete_movie(client, setup_database, username, password):
    # Login with the user 1
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Delete Movie
    response = client.delete("/movies/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Movie deleted successfully"

    # Delete Movie with invalid id
    response = client.delete("/movies/4", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "Movie not found"}

    # Delete Movie with invalid user
    response = client.delete("/movies/3", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    data = response.json()
    assert data == {"detail": "You are not authorized to delete"}    


# # # # ========================
# # # # Rating Endpoint test
# # # # ========================
    
# # Get ratings for a movie without rating
@pytest.mark.parametrize("username1, password1, username2, password2", [("testuser", "testpassword","testuser2","testpassword2")])
def test_get_rating(client, setup_database, username1, password1,username2,password2):

    # Rate without authenticating
    response = client.post(
        "/ratings/",
        json={"movie_id": 1, "rating": 4}
    )
    assert response.status_code == 401
    data = response.json()
    assert data == {"detail": "Not authenticated"}
    
    # login with user 1
    response = client.post("/login", data={"username": username1, "password": password1})
    assert response.status_code == 200
    token = response.json()["access_token"]
    movie_2 = 2
    rating_value = 4

    # Get rating for a movie without rating
    response = client.get("/ratings/",
                          params={"movie_id": movie_2} ,
                           headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
    data = response.json()
    assert data == {"detail": "No ratings found for movie with id 2"}

    # Rate a non-existent movie
    response = client.post(
        "/ratings/",
        json={"movie_id": 1, "rating": rating_value},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Movie with id 1 does not exist"

    # Rate a Movie
    response = client.post(
        "/ratings/",
        json={"movie_id": movie_2, "rating": rating_value},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["movie_id"] == movie_2
    assert data["movie_title"] == "Test Book 2"
    assert data["average_rating"] == 4.0

    # Get rating for a movie with rating
    response = client.get("/ratings/",
                          params={"movie_id": movie_2} ,
                           headers={"Authorization": f"Bearer {token}"})
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["movie_id"] == movie_2
    assert data["average_rating"] == 4.0
    assert data["movie_title"] == "Test Book 2"

    # Rate a Movie with invalid rating
    response = client.post(
        "/ratings/",
        json={"movie_id": movie_2, "rating": 6},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422

    # Login with user 2
    response = client.post("/login", data={"username": username2, "password": password2})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Rate movie 2 with user 2
    response = client.post(
        "/ratings/",
        json={"movie_id": movie_2, "rating": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["movie_id"] == movie_2
    assert data["average_rating"] == 3.5
    assert data["movie_title"] == "Test Book 2"


# # # # ========================
# # # # comments Endpoint test
# # # # ========================

# @pytest.mark.parametrize("username1, password1, username2, password2", [("testuser", "testpassword","testuser2","testpassword2")])
# def test_get_comments(client, setup_database, username1, password1,username2,password2):

#     # Get comments for a movie without comments
#     response = client.get("/comments/2")
#     assert response.status_code == 404
#     data = response.json()
    
#     # login with user 1
#     response = client.post("/login", data={"username": username1, "password": password1})
#     assert response.status_code == 200
#     token = response.json()["access_token"]

#     # Add comments to a movie
#     response = client.post(
#         "/comments/",
#         json={"movie_id": 2, "content": "Test Comment"},
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["movie_id"] == 2
#     assert data["content"] == "Test Comment"

#     # Get comments for a movie with comments
#     response = client.get("/comments/2")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 1
#     assert data[0]["content"] == "Test Comment"
