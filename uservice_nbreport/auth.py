"""Authentication with GitHub and LSST the Docs.
"""

__all__ = ('github_token_auth', 'requires_github_org_membership', 'ltd_login')

from functools import wraps
from urllib.parse import urljoin

from flask import g, current_app
from flask_httpauth import HTTPBasicAuth

import requests
import structlog
from apikit import BackendError

from .exceptions import GitHubAuthenticationError, GitHubAuthorizationError


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
       call is attached to ``flask.g.github_user_data``

    3. The GitHub username is attached to ``flask.github_user``.

    4. The GitHub token is attached to ``flask.github_token``.
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
    raise GitHubAuthenticationError()


def requires_github_org_membership():
    """Test GitHub organization membership (to be used as a route decorator).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_github_org_membership()
                return f(*args, **kwargs)

            except (GitHubAuthenticationError, GitHubAuthorizationError):
                raise

            except Exception as e:
                raise BackendError(
                    'Unexpected server error during authentication.',
                    status_code=500,
                    content=str(e)
                )
        return decorated_function
    return decorator


def verify_github_org_membership():
    """Verify that the authenticated GitHub user is a member of the
    GitHub organization configured in the ``AUTHORIZED_GITHUB_ORG`` config.

    This function is used by `requires_github_org_membership`.

    Raises
    ------
    GitHubAuthenticationError
        Raised if GitHub authentication has not occured.
    GitHubOrgAuthorizationError
        Raised if the user is not a member of the required GitHub
        organization.
    """
    try:
        username = g.github_user
        token = g.github_token
    except AttributeError:
        raise GitHubAuthenticationError()

    # Access the user's organization memberships (need to iterate)
    # https://developer.github.com/v3/orgs/#list-your-organizations
    org_data = iter_github_endpoint(
        'https://api.github.com/user/orgs',
        auth=(username, token),
        headers={'Accept': 'application/vnd.github.v3+json'}
    )

    org_list = [org['login'] for org in org_data]
    if current_app.config['AUTHORIZED_GITHUB_ORG'] not in org_list:
        raise GitHubAuthorizationError()


def iter_github_endpoint(url, verb='GET', auth=None, headers=None,
                         current_data=None):
    """Perform a request and follow GitHub-style pagination.
    """
    if current_data is None:
        current_data = []

    response = requests.request(
        verb,
        url,
        auth=auth,
        headers=headers)
    response.raise_for_status()

    current_data.extend(response.json())

    try:
        next_url = response.links['next']['url']
    except (AttributeError, KeyError):
        return current_data

    return iter_github_endpoint(
        next_url, verb=verb, auth=auth, headers=headers,
        current_data=current_data)


def ltd_login():
    """Log into LSST the Docs Keeper API server (used as a route decorator).

    Notes
    -----
    This decorator **must** be applied after GitHub authentication and
    authorization (e.g., `github_token_auth`, and
    `requires_github_org_membership`).

    This decorator adds two attributes to ``flask.g``:

    - ``flask.g.ltd_user``: The username this app uses with LSST the Docs
      Keeper.

    - ``flask.g.ltd_token``: The limited-time token the app can use during
      this route response.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                get_ltd_token()
                return f(*args, **kwargs)

            except Exception as e:
                raise BackendError(
                    'Unexpected error while authentication with LSST the '
                    'Docs ({0})'.format(current_app.config['KEEPER_URL']),
                    status_code=500,
                    content=str(e))
        return decorated_function
    return decorator


def get_ltd_token():
    """Request and add the LTD Keeper token to the request context.

    This function is meant to be called by the `ltd_login` decorator.
    """
    # Double check that we already logged-in with GitHub
    if not hasattr(g, 'github_token'):
        raise GitHubAuthenticationError()

    response = requests.get(
        urljoin(current_app.config['KEEPER_URL'], '/token'),
        auth=(current_app.config['KEEPER_USERNAME'],
              current_app.config['KEEPER_PASSWORD'])
    )
    response.raise_for_status()

    g.ltd_user = current_app.config['KEEPER_USERNAME']
    g.ltd_token = response.json()['token']
