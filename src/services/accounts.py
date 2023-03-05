from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token

from db.crypto_pass import PBKDF2StoragePassword
from db.models import User
from db.storage.user_storage import PostgresUserStorage
from db.storage.device_storage import DeviceStorage
from db.storage.history_storage import HistoryAuthStorage


class AccountService:
    def __init__(self, user: User=None):
        self.user = user

    def _generate_password(self, login, email):
        password_string = login + email
        password_checker = PBKDF2StoragePassword()
        return password_checker.create_hash(password_string)
        
    def create(self, login: str, email: str, password: str=None):
        user_storage = PostgresUserStorage()
        if not password:
            password = self._generate_password(login, email)
        self.user = user_storage.create(
            login=login,
            password=password,
            email=email
        )
        return self.user

    def get_user_tokens(self):
        identity = str(self.user.id)
        access_token = create_access_token(identity)
        refresh_token = create_refresh_token(identity)
        return access_token, refresh_token

    def update_user_info(self, user_agent):
        history_storage = HistoryAuthStorage()
        device_storage = DeviceStorage()
        devices_user = list(device_storage.filter(name=user_agent, owner=self.user))

        if not devices_user:
            # Отправить пользователю уведомление о том, что произошел вход с другого устройства.
            # Будет реализовано в следующем спринте.

            # сохраняем новое устройство пользователя.
            current_device = device_storage.create(name=user_agent, owner=self.user)
        else:
            current_device = device_storage.get(name=user_agent, owner=self.user)

            # делаем запись в таблицу history_auth.
        history_storage.create(
         user=self.user, device=current_device, date_auth=datetime.now()
        )
