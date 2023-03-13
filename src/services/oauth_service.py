from __future__ import annotations

from abc import ABC

from core.oauth import oauth_client
from core.enums import Providers
from db.models import SocialAccount
from db.postgres import db
from services.exceptions import SocialAccountError
from services.schemas import get_schema_user_info


class OAuthService(ABC):
    def __init__(self, provider_name):
        self.name = provider_name

    def get_user_info(self, *args, **kwargs):
        client = oauth_client.create_client(self.name)
        token = client.authorize_access_token()
        access_token = token.get("access_token")
        raw_user_info = client.userinfo(params={"access_token": access_token})
        return get_schema_user_info(self.name)(**raw_user_info)

    def remove(self, user_id):
        account = SocialAccount.query.filter_by(
            user_id=user_id,
            social_name=self.name,
        ).first()
        if not account:
            raise SocialAccountError
        db.session.delete(account)
        db.session.commit()


class YandexOAuthService(OAuthService):

    pass


class MailOAuthService(OAuthService):

    pass


class VkOAuthService(OAuthService):
    def get_user_info(self, *args, **kwargs):
        client = oauth_client.create_client(self.name)
        token = client.authorize_access_token()
        return get_schema_user_info(self.name)(**token)


def get_provider(provider_name: str) -> OAuthService:
    """По имени провайдера получить сервси для авторизации."""
    providers_to_service: dict = {
        Providers.VK.value: VkOAuthService,
        Providers.YANDEX.value: YandexOAuthService,
        Providers.MAIL.value: MailOAuthService,
    }

    if provider_name not in providers_to_service:
        raise KeyError(f"Provider {provider_name} dont exists.")
    return providers_to_service[provider_name](provider_name)
