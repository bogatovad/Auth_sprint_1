import pytest
from services.application import create_app
from db.postgres import init_db, db
from random import randint
from flask_jwt_extended import create_refresh_token, create_access_token

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
    return create_access_token(user["login"])


@pytest.fixture
def refresh_token(user):
    return create_refresh_token(user['login'])


@pytest.fixture
def auth_access_header(access_token):
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def auth_refresh_header(refresh_token):
    return {"Authorization": f"Bearer {refresh_token}"}
