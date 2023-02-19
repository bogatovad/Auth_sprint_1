import pytest
import http
from main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def login():
    return f"login"


@pytest.fixture
def password():
    return "password"


@pytest.fixture
def user(login, password):
    return {
        "login": login,
        "password": password
    }


def test_signup_ok(client, login, password, user):
    response = client.post(
        path="/api/v1/auth/signup",
        data={
            "login": login,
            "password": password,
        },
    )

    assert response.status_code == http.HTTPStatus.CREATED

    result = response.json
    assert result == {'message': f"User '{login}' successfully created"}

