from __future__ import annotations
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from commands.register_commands import Command
from core.config import auth_config
from core.oauth import init_oauth
from db.postgres import init_db
from services.application import create_app
from flask import request
from tracer import configure_tracer


app = create_app()
app.secret_key = "super secret key"


@app.before_request
def before_request():
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        raise RuntimeError("request id is required")


if auth_config.tracer_enabled:
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)

command = Command(app)
command.register_command()
init_db(app)
init_oauth(app)
app.app_context().push()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
