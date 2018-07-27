"""Authentication with GitHub.
"""

__all__ = ('github_token_auth',)

from flask import g
from flask_httpauth import HTTPBasicAuth

import requests
import structlog

from .exceptions import ValidationError


github_token_auth = HTTPBasicAuth()
"""GitHub personal access token-based authentication.
"""


@github_token_auth.verify_password
def verify_github_token(username, token):
    """Verify the GitHub token provided as a password for basic auth.

    Parameters
    ----------
    username : `str`
        GitHub username.
    token : `str`
        GitHub personal access token (though in principle, a GitHub password
        could be used, which is not encouraged).

    Returns
    -------
    bool
        Returns `True` if the credential authenticate with GitHub.
        `False` otherwise.

    Notes
    -----
    In addition to authenticating a user, this handler has two useful side
    effects:

    1. The username is bound to the structlog logger with a ``github_user``
       key.

    2. The data structured returned by the ``GET https://api.github.com/user``
       call is attached to ``flask.g`` under the ``github_user_data``
       attribute.
    """
    if username is None:
        return False

    # Bind the username to the logger
    structlog.get_logger().bind(github_user=username)

    response = requests.get(
        'https://api.github.com/user',
        auth=(username, token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )
    if response.status_code >= 300:
        # Means authentication failed
        return False

    # Store user data now that they're authenticated
    g.github_user = username
    g.github_token = token
    g.github_user_data = response.json()

    return True


@github_token_auth.error_handler
def unauthorized_token_access():
    """Callback for when the `github_token_auth` authentication fails that
    emits a 401 status and json-formatted error message.
    """
    raise ValidationError(
        'Please authenticate with a GitHub username and personal access '
        'token.',
        status_code=401
    )
