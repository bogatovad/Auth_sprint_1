import pytest

from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def login():
    return "login"


@pytest.fixture
def password():
    return "password"


@pytest.fixture
def user(login, password):
    return {"login": login, "password": password}
