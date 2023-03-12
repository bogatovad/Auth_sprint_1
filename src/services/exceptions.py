from __future__ import annotations


class AuthError(Exception):
    """Исключение, поднимающеся при некорректных данных для аутентификации."""

    def __init__(self, message="Login or password are incorrect."):
        self.message = message
        super().__init__(self.message)


class DuplicateUserError(Exception):
    """Исключение, поднимающеся при создании пользователя с логином уже существующим."""

    def __init__(self, message="User with such login already exist."):
        self.message = message
        super().__init__(self.message)


class SocialAccountError(Exception):
    """Исключение, поднимающеся если удаляемого аккаунта нет."""

    def __init__(self, message="Social account dont exist."):
        self.message = message
        super().__init__(self.message)
