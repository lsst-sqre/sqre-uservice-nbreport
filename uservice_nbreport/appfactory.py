"""Create the Flask application.
"""

__all__ = ('create_flask_app',)

from apikit import APIFlask

from .version import get_version


def create_flask_app():
    """Create the Flask app with /nbreport routes behind api.lsst.codes.
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

    # register blueprints with the routes
    from .routes import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/nbreport')

    return app
