from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import config

from .extensions import db


db = SQLAlchemy()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://auth:qwerty123@postgres/auth'
    db.init_app(app)
