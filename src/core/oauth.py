from db.extensions import oauth_client

oauth_client.register(
    name='yandex',
    client_id='020bbccb33d34998af290fca2083d052',
    client_secret='07ec9f01a665460dbced7e794e62d375',
    access_token_url='https://oauth.yandex.ru/token',
    access_token_params=None,
    authorize_url='https://oauth.yandex.ru/authorize',
    authorize_params=None,
    userinfo_endpoint='https://login.yandex.ru/info?',
    api_base_url='https://oauth.yandex.ru/',
    client_kwargs=None,
)
