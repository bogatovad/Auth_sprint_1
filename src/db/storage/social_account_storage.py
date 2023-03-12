from __future__ import annotations

from db.models import SocialAccount
from db.models import User
from db.postgres import db


class SocialAccountStorage:
    @staticmethod
    def create(user: User, social_id: str, social_name: str):
        social_account = SocialAccount(
            user=user,
            social_id=social_id,
            social_name=social_name,
        )
        db.session.add(social_account)
        db.session.commit()
        return social_account

    @staticmethod
    def get_account(social_id: str, social_name: str):
        return SocialAccount.query.filter_by(
            social_id=social_id,
            social_name=social_name,
        ).first()
