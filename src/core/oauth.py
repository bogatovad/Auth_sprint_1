from __future__ import annotations

from authlib.integrations.flask_client import OAuth
from flask import Flask
from core.config import vk_config, yandex_config, mail_config

oauth_client = OAuth()


for config in (vk_config, yandex_config, mail_config):
    oauth_client.register(**config)

def init_oauth(app: Flask):
    oauth_client.init_app(app)


def get_client():
    return oauth_client
