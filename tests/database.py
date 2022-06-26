
#  ! Everything is moved to confest.py file for utilizing the feature of pytest

import pytest
from alembic import command

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test"

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
