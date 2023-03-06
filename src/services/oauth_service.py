from pydantic import BaseModel

from db.postgres import db
from db.models import SocialAccount, User
from core.oauth import oauth_client


class OAuthProviderInfo(BaseModel):
    id: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None   


class OAuthService:
    def __init__(self, provider_name): 
        self.name = provider_name

    def get_user_info(self):
        client = oauth_client.create_client(self.name)
        token = client.authorize_access_token()
        raw_user_info = token.get("userinfo")
        if not raw_user_info:
            raw_user_info = client.userinfo()
        if self.name == 'yandex':
            self.user_info = OAuthProviderInfo(
            email=raw_user_info['default_email'],
            **raw_user_info
            )
        else:
            self.user_info = OAuthProviderInfo(**raw_user_info)
        return self.user_info

    def create_social_account(self, user: User) -> SocialAccount:
        account = SocialAccount(
            user_id=user.id,
            social_id=self.user_info.id,
            social_name=self.name,
            email=self.user_info.email
        )
        db.session.add(account)
        db.session.commit()
        return account

    def get_social_account(self):
        return SocialAccount.query.filter_by(social_id=self.user_info.id, social_name=self.name).one_or_none()