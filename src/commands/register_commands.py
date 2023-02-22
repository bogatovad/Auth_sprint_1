import click

from commands.user import create_superuser_command


class Command:
    """Класс, регистрирует команды для CLI."""

    def __init__(self, app):
        self.app = app
        self.commands = []

        @app.cli.command("create-superuser")
        @click.argument("login")
        @click.argument("password")
        @click.argument("email")
        def create_superuser(login, password, email):
            create_superuser_command(login, password, email)

        self.commands.append(create_superuser)

    def register_command(self):
        for command in self.commands:
            self.app.cli.add_command(command)
