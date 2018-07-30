"""Create the Flask application.
"""

__all__ = ('create_flask_app',)

import os

from apikit import APIFlask

from .version import get_version
from .cli import add_app_commands
from .config import config_profiles


def create_flask_app(profile=None):
    """Create the Flask app with /nbreport routes behind api.lsst.codes.

    Parameters
    ----------
    profile : `str`, optional
        Application profile: "production", "dev", or "test".

    Returns
    -------
    app : apikit.APIFlask
        Flask application instance.
    """
    app = APIFlask(
        name="uservice-nbreport",
        version=get_version(),
        repository="https://github.com/sqre-lsst/uservice-nbreport",
        description="Publication service for LSST notebook-based reports",
        route=["/", "/nbreport"],
        auth={"type": "basic",
              "data": {"username": "",
                       "password": ""}})

    # Configurations
    if profile is None:
        profile = os.getenv('NBREPORT_PROFILE', 'dev')
    app.config.from_object(config_profiles[profile])

    # register blueprints with the routes
    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/nbreport')

    # Add custom Flask CLI subcommands
    add_app_commands(app)

    return app
