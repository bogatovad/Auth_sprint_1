from abc import ABC, abstractmethod

from db.models import User
from db.postgres import db


class BaseUserStorage(ABC):
    """Интерфейс для взаимодействия с таблицей пользователя."""

    @abstractmethod
    def exists(self, login: str):
        pass

    @abstractmethod
    def create(self, login: str, password: str, email: str):
        pass

    @abstractmethod
    def get(self, login: str):
        pass

    @abstractmethod
    def change(self):
        pass


class PostgresUserStorage(BaseUserStorage):
    """Реализация интерфейса для бд PostgreSQL."""

    def exists(self, login: str) -> bool:
        user = User.query.filter_by(login=login).first()
        return True if user is not None else False

    def create(self, login: str, password: str, email: str) -> User:
        user = User(login=login, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return user

    def get(self, login: str) -> User:
        return User.query.filter_by(login=login).first()

    def change(self):
        pass

    def search(self, **kwargs):
        return User.query.filter_by(**kwargs).one_or_none()

    def get_by_id(self, id):
        return User.query.filter_by(id=id).first()

