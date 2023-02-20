import random

import pytest
from main import app
from services.application import create_app
from db.postgres import init_db, db
from random import randint

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    init_db(app)
    app.app_context().push()
    db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def login():
    return f"login_{randint(1, 1000)}"


@pytest.fixture(scope='session')
def password():
    return "password"


@pytest.fixture
def email():
    return "somemail@mail.ru"


@pytest.fixture
def user(login, password, email):
    return {"login": login, "password": password, "email": email}


@pytest.fixture
def access_token(user):
    # TODO Remove hardcode
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NjgyMjUyOSwianRpIjoiYTFkYjkxOTctNmEwYy00NGU4LWFjMWItMTZmZDY3MDExNWRhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InNvbWV0aGluZyIsIm5iZiI6MTY3NjgyMjUyOSwiZXhwIjo3NjMyNjQyMjUyOX0.DEQDfGARGbiK5_XbWdAR2AdzRVbyc64gVdYQMbvuEBU"


@pytest.fixture
def refresh_token(user):
    # TODO Remove hardcode
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NjgyMjUyOSwianRpIjoiYzhkZDM1N2ItM2VkZC00NjUwLWIyZTEtY2I1MWZhNDg0NjI5IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJzb21ldGhpbmciLCJuYmYiOjE2NzY4MjI1MjksImV4cCI6MTc1NDU4MjUyOX0.l8BSAF2l4dWuAnEqjghVCIW1ZzPUw6sfdMf1Q0VMt5Y"


@pytest.fixture
def auth_access_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def auth_refresh_header(refresh_token):
    return {"Authorization": f"Bearer {refresh_token}"}
