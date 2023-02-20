class AuthError(Exception):
    """Исключение, поднимающеся при некорректных данных для аутентификации."""
    def __init__(self, message="Login or password are incorrect."):
        self.message = message
        super().__init__(self.message)
