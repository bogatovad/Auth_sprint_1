import http
from db.redis_client import redis_client

AUTH_URL = "/api/v1/auth"


def test_signup_ok(client, user, login, password, email):
    response = client.post(
        path=f"{AUTH_URL}/signup",
        data=user
    )

    assert response.status_code == http.HTTPStatus.CREATED

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


def test_nonexistent_login(client):
    response = client.post(
        path=f"{AUTH_URL}/login",
        data={
            "login": "nonexistent",
            "password": "password",
        },
    )

    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_logout_ok(client, auth_access_header):
    response = client.post(
        path=f"{AUTH_URL}/logout",
        headers=auth_access_header,
    )
    assert response.status_code == http.HTTPStatus.OK


def test_refresh_ok(client, auth_refresh_header):
    response = client.get(
        path=f"{AUTH_URL}/refresh",
        headers=auth_refresh_header,
    )
    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert "access_token" in result
    assert "refresh_token" in result

