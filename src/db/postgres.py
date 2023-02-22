from flask import Flask

from core.config import config

from .extensions import db, migrate


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://app:123qwe@postgres_auth/postgres"
    db.init_app(app)
    migrate.init_app(app, db)