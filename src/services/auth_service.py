from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from db.crypto_pass import PBKDF2StoragePassword
from db.models import User
from db.storage.user_storage import PostgresUserStorage
from services.exceptions import AuthError, DuplicateUserError


class BaseAuth(ABC):
    """Базовый класс для аутентефикации пользователя."""

    @abstractmethod
    def signup(self, *args, **kwargs):
        """Метод регистрации пользователя."""
        pass

    @abstractmethod
    def login(self, *args, **kwargs):
        """Метод аутентефикации."""
        pass


class JwtAuth(BaseAuth):
    """Реализация аутентефикации на jwt-токенах."""

    def signup(self, *args, **kwargs) -> User:
        """Реализаия метода регистрации пользователя."""
        login, password, email = args
        storage = PostgresUserStorage()
        password_checker = PBKDF2StoragePassword()

        if storage.exists(login):
            raise DuplicateUserError()

        return storage.create(
            login=login,
            password=password_checker.create_hash(password),
            email=email,
        )

    def login(self, *args, **kwargs) -> User:
        login, password = args
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
