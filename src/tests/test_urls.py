import http
from db.redis_client import redis_client
from flask_jwt_extended import get_jwt_identity, get_jwt
from db.storage.user_storage import PostgresUserStorage
from services import exceptions

AUTH_URL = "/api/v1/auth"


def test_signup_ok(client, user, login):
    response = client.post(
        path=f"{AUTH_URL}/signup",
        data=user
    )
    assert response.status_code == http.HTTPStatus.CREATED
    result = response.json
    assert result == {"message": f"User '{login}' successfully created"}

    storage = PostgresUserStorage()
    assert storage.exists(login=login) is True


def test_signup_existent_user(client, user):
    response = client.post(
        path=f"{AUTH_URL}/signup",
        data=user
    )
    assert response.status_code == http.HTTPStatus.CONFLICT


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
    assert response.json["message"] == exceptions.AuthError().message


def test_login_without_password(client):
    response = client.post(
        path=f"{AUTH_URL}/login",
        data={
            "login": "nonexistent",
        },
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json["message"] == {'password': 'Password required'}


def test_login_wihout_credentials(client):
    response = client.post(
        path=f"{AUTH_URL}/login",
        data={},
    )

    assert response.status_code == http.HTTPStatus.BAD_REQUEST


def test_logout_ok(client, auth_access_header):
    response = client.post(
        path=f"{AUTH_URL}/logout",
        headers=auth_access_header,
    )
    assert response.status_code == http.HTTPStatus.OK
    # Проверка, что access токен записался в базу невалидных токенов
    assert redis_client.db_for_invalid_access.get(get_jwt()['jti']) is not None


def test_logout_without_access_token(client):
    response = client.post(
        path=f"{AUTH_URL}/logout",
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


    new_refresh = result["refresh_token"]
    token_in_redis = redis_client.db_for_refresh.get(get_jwt_identity())
    # Проверка, что refresh токен записался в базу
    assert token_in_redis is not None
    # Проверка, что токен в редисе и новый полученный совпадают
    assert new_refresh == token_in_redis.decode()


def test_refresh_without_refresh_token(client):
    response = client.get(
        path=f"{AUTH_URL}/refresh",
    )
    assert response.status_code == http.HTTPStatus.UNAUTHORIZED


def test_refresh_with_access_token(client, auth_access_header):
    response = client.get(
        path=f"{AUTH_URL}/refresh",
        headers=auth_access_header,
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY


def test_logout_with_refresh_token(client, auth_refresh_header):
    response = client.post(
        path=f"{AUTH_URL}/logout",
        headers=auth_refresh_header,
    )
    assert response.status_code == http.HTTPStatus.UNPROCESSABLE_ENTITY
