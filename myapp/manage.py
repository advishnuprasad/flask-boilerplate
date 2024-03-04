import click
from flask.cli import with_appcontext


@click.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from myapp.extensions import db
    from myapp.models import User

    click.echo("create user")
    user = User(
        username="admin", email="admin@example.com", password="password", active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")
