from flask import Flask

from core.config import Config

from .extensions import db, migrate


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)
