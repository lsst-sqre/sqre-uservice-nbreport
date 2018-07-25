"""Command line subcommands for the Flask CLI.

Flask CLI subcommands are implemented with Click. The application factory
(`uservice_nbreport.appfactory`) registers these.
"""

__all__ = ('add_app_commands', 'version_command')

import click
from flask.cli import with_appcontext

from .version import get_version


def add_app_commands(app):
    """Add custom flask subcommands to the Flask app.
    This function is called by `keeper.appfactory.create_flask_app`.
    """
    app.cli.add_command(version_command)


@click.command('version')
@with_appcontext
def version_command():
    """Print the LTD Keeper application version.

    Alternatively, to get the Flask and Python versions, run::

       flask --version
    """
    click.echo(get_version())
