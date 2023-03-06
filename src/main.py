from opentelemetry.instrumentation.flask import FlaskInstrumentor

from commands.register_commands import Command
from db.postgres import init_db
from services.application import create_app
from flask import request
from tracer import configure_tracer


app = create_app()


@app.before_request
def before_request():
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        raise RuntimeError("request id is required")


configure_tracer()
FlaskInstrumentor().instrument_app(app)

command = Command(app)
command.register_command()
init_db(app)
app.app_context().push()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
