from pydantic import BaseModel, Field

from core.enums import Providers

class OAuthProviderInfo(BaseModel):
    """Схема для получения данных о пользователе."""

    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None


class VkOAuthProviderInfo(OAuthProviderInfo):
    """Схема для получения данных о пользователе из vk."""

    id: str | None = Field(alias='user_id')


class YandexOAuthProviderInfo(OAuthProviderInfo):
    """Схема для получения данных о пользователе из yandex."""

    id: str | None
    email: str | None = Field(alias='default_email')


class MailOAuthProviderInfo(OAuthProviderInfo):
    """Схема для получения данных о пользователе из vk."""

    id: str | None = Field(alias='client_id')


def get_schema_user_info(provider_name: str) -> OAuthProviderInfo:
    """По имени провайдера получить схему."""

    providers_to_schema: dict = {
        Providers.VK.value: VkOAuthProviderInfo,
        Providers.YANDEX.value: YandexOAuthProviderInfo,
        Providers.MAIL.value: MailOAuthProviderInfo
    }
    if provider_name not in providers_to_schema:
        raise KeyError(f'Schema for proveder {provider_name} dont exists.')
    return providers_to_schema[provider_name]