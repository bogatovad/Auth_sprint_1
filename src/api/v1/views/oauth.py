from http import HTTPStatus
import requests

from flask import Blueprint, jsonify, make_response, url_for, request
from authlib.integrations.flask_client import OAuth

from db.storage.user_storage import PostgresUserStorage
from core.oauth import oauth_client
from services.accounts import AccountService
from services.oauth_service import OAuthService


oauth = Blueprint("oauth", __name__, url_prefix="/api/v1/oauth")


@oauth.get("/login/<string:provider_name>")
def login(provider_name):
    client = oauth_client.create_client(provider_name)
    redirect_uri = url_for(f'oauth.authorize', _external=True, provider_name=provider_name)    
    return client.authorize_redirect(redirect_uri)


@oauth.get("/authorize/<string:provider_name>")
def authorize(provider_name):
    oauth_service = OAuthService(provider_name)
    user_info = oauth_service.get_user_info()
    user_storage = PostgresUserStorage()
    social_account = oauth_service.get_social_account()
    if social_account:
        user = user_storage.get_by_id(social_account.user_id)    
    else:        
        user = user_storage.search(email=user_info.email)
        if not user:
            account = AccountService()
            user = account.create(
            login=user_info.email,
            email=user_info.email
        )
        oauth_service.create_social_account(user=user)
    user_account = AccountService(user)
    access_token, refresh_token = user_account.get_user_tokens()
    user_account.update_user_info(request.headers.get('user_agent'))
    return make_response(
            jsonify(access_token=access_token, refresh_token=refresh_token),
            HTTPStatus.OK,
        )

