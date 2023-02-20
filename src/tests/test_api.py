import http
from db.redis import redis_client
from db.models import User

AUTH_URL = "/api/v1/auth"


def test_signup_ok(client, user, login):
    response = client.post(
        path=f"{AUTH_URL}/signup",
        data=user
    )
    assert response.status_code == http.HTTPStatus.OK
    result = response.json
    assert result == {"message": f"User '{login}' successfully created"}


def test_login_ok(client, login, password):
    response = client.post(
        path=f"{AUTH_URL}/login",
        data={
            "login": login,
            "password": password,
        },
    )

    assert response.status_code == http.HTTPStatus.OK

    result = response.json

    assert "access_token" in result
    assert "refresh_token" in result

    # test logout with access token.

    bearer_header = {"Authorization": f"Bearer {result['refresh_token']}"}
    response = client.post(
        path=f"{AUTH_URL}/logout",
        headers=bearer_header,
    )
    assert response.status_code == http.HTTPStatus.OK


def test_nonexistent_login(client):
    response = client.post(
        path=f"{AUTH_URL}/login",
        data={
            "login": "nonexistent",
            "password": "password",
        },
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_refresh_ok(client, auth_refresh_header):
    response = client.get(
        path=f"{AUTH_URL}/refresh",
        headers=auth_refresh_header,
    )
    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert "access_token" in result
    assert "refresh_token" in result

    token_in_redis = redis_client.db_for_refresh.get(result["refresh_token"])
    assert token_in_redis is not None
