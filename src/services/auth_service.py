from abc import ABC, abstractmethod
from http import HTTPStatus

from db.crypto_pass import PBKDF2StoragePassword
from db.models import User
from db.storage.user_storage import PostgresUserStorage
from services.exceptions import AuthError


class BaseAuth(ABC):
    """Базовый класс для аутентефикации пользователя."""

    @abstractmethod
    def signup(self):
        """Метод регистрации пользователя."""
        pass

    @abstractmethod
    def login(self):
        """Метод аутентефикации."""
        pass

    @abstractmethod
    def logout(self):
        """Метод осуществялющий выход из сеанса."""
        pass


class JwtAuth(BaseAuth):
    """Реализация аутентефикации на jwt-токенах."""

    def signup(self, login: str, password: str, email: str):
        """Реализаия метода регистрации пользователя."""
        storage = PostgresUserStorage()
        password_checker = PBKDF2StoragePassword()

        if storage.exists(login):
            return {"message": f"User '{login}' exists. Choose another login."}, HTTPStatus.CONFLICT

        return storage.create(
            login=login,
            password=password_checker.create_hash(password),
            email=email
        )

    def login(self, login: str, password: str) -> User:
        storage = PostgresUserStorage()
        password_checker = PBKDF2StoragePassword()

        # Проверка корректности логина.
        if not storage.exists(login):
            raise AuthError()

        user = storage.get(login=login)

        # Проверка корректности пароля.
        if not password_checker.check_password(password, user.password):
            raise AuthError()

        return user

    def logout(self):
        pass
