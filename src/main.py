from db.postgres import db, init_db
from services.application import create_app
import click
from services.auth_service import JwtAuth
from services.exceptions import DuplicateUserError

app = create_app()


@app.cli.command("create-superuser")
@click.argument("login")
@click.argument("password")
@click.argument("email")
def create_superuser(login, password, email):
    init_db(app)
    auth_service = JwtAuth()
    try:
        user = auth_service.signup(login, password, email)
        click.echo(f"User {user} created")
    except DuplicateUserError:
        click.echo(f"User {login} already exists.")


def main():
    init_db(app)
    app.app_context().push()
    db.create_all()

    app.run(host="0.0.0.0", port=5555, debug=True)


if __name__ == "__main__":
    main()
