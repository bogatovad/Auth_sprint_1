from __future__ import annotations

from commands.register_commands import Command
from core.oauth import init_oauth
from db.postgres import init_db
from services.application import create_app

app = create_app()
app.secret_key = "super secret key"
command = Command(app)
command.register_command()
init_db(app)
init_oauth(app)
app.app_context().push()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True)
