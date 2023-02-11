from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from core.config import config


db = SQLAlchemy()


def init_db(app: Flask):
    print(config.SQLALCHEMY_DATABASE_URI)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    db.init_app(app) 