from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import config

from .extensions import db


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    db.init_app(app)


db = SQLAlchemy()


def init_db(app: Flask):
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://app:123qwe@postgres/auth_database"
    db.init_app(app)
