from commands.register_commands import Command
from db.postgres import init_db
from services.application import create_app
from db.extensions import oauth_client

app = create_app()
command = Command(app)
command.register_command()
init_db(app)
oauth_client.init_app(app)
app.app_context().push()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
