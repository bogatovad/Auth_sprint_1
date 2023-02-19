import http


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
    assert result == {"message": f"User '{login}' successfully created"}


def test_login_ok(client, user, login, password):
    response = client.post(
        path="/api/v1/auth/login",
        data={
            "login": login,
            "password": password,
        },
    )

    assert response.status_code == http.HTTPStatus.OK

    result = response.json
    assert "access_token" in result
    assert "refresh_token" in result
