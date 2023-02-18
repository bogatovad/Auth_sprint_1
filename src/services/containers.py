from dependency_injector import containers
from dependency_injector.ext import flask
from flask import Flask


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    app = flask.Application(Flask, __name__)
