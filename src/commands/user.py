import click

from db.models import Role
from services.auth_service import JwtAuth
from services.exceptions import DuplicateUserError


def create_superuser_command(login, password, email):
    """Команда для создания супер пользователя."""
    auth_service = JwtAuth()
    try:
        admin_role = Role.get_or_create(name='superuser')
        user = auth_service.signup(login, password, email)
        user.add_role(admin_role)
        click.echo(f"User {user} created")
    except DuplicateUserError:
        click.echo(f"User {login} already exists.")
