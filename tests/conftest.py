from venv import create
import pytest
from alembic import command

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.main import app
from app import schemas, models
from app.config import devSettings
from app.database import get_db, Base
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f"postgresql://{devSettings.DATABASE_USERNAME}:{devSettings.DATABASE_PASSWORD}@{devSettings.DATABASE_HOSTNAME}:{devSettings.DATABASE_PORT}/{devSettings.DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# # Dependency


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)  # Dropping all the tables
    Base.metadata.create_all(bind=engine)  # Creating all the tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Dropping all the tables
    


@pytest.fixture()
def client(session):

    # Run our code before we run our tests
    # Base.metadata.create_all(bind=engine) # Creating all the tables
    # yield TestClient(app)

    # Run our code after our test finishes
    # Base.metadata.drop_all(bind=engine) # Dropping all the tables

    # Drop tables first and then create a fresh ones and then perform the tests
    # Base.metadata.drop_all(bind=engine)  # Dropping all the tables
    # Base.metadata.create_all(bind=engine)  # Creating all the tables
    # yield TestClient(app)

    # Using Alembic
    # command.upgrade("head")
    # yield TestClient(app)
    # command.downgrade("base")

    # Dependent Fixtures
    # Benifit of this is we can access the client object as well as the Database object with session from which we can make queries
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client, session):
    user_data = {"email": "abc@gmail.com", "password": "123"}

    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print("Test User: ", res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client, session):
    user_data = {"email": "abcd@gmail.com", "password": "123"}

    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print("Test User: ", res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_create_posts(session, test_user, test_user2):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)

    session.add_all(posts)

    session.commit()

    return session.query(models.Post).all()
