import hashlib
import os
from abc import ABC, abstractmethod


class StoragePassword(ABC):
    @abstractmethod
    def create_hash(self, password: str):
        pass

    @abstractmethod
    def check_password(self, password: str):
        pass


class PBKDF2StoragePassword(StoragePassword):
    @staticmethod
    def _generate_key(password: str, salt: bytes):
        algorithm: str = 'sha256'
        return hashlib.pbkdf2_hmac(
            algorithm,
            password.encode('utf-8'),
            salt,
            100000
        )

    def create_hash(self, password: str):
        length_salt: int = 32
        salt: bytes = os.urandom(length_salt)
        key_pbkdf2_hmac = self._generate_key(password, salt)
        return key_pbkdf2_hmac + salt

    @staticmethod
    def _extract_salt_and_key(password):
        return password[:32], password[32:]

    def check_password(self, password: str, password_in_datastage: bytes):
        key_pbkdf2_hmac, salt = self._extract_salt_and_key(password_in_datastage)
        new_key_pbkdf2_hmac = self._generate_key(password, salt)
        return new_key_pbkdf2_hmac == key_pbkdf2_hmac

