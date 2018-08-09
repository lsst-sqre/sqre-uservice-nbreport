"""Pytest fixtures.
"""

from base64 import b64encode

import pytest

from uservice_nbreport.appfactory import create_flask_app

TEST_USER = 'testuser'
TEST_TOKEN = 'testtoken'


@pytest.fixture
def client():
    """Client for testing the REST API endpoints, as a pytest fixture.

    Notes
    -----
    The app is run with the "test" profile, meaning that the ``TESTING`` config
    flag is activate. Any app exception gets passed to the client code rather
    than generating a 500 error.

    You can either use this client directly, or within a context manager.
    Using the client as a context manager allows access to application
    context, like ``flask.g``, after the response is completed. See
    test_routes_login.py for examples.
    """
    app = create_flask_app(profile='test')
    client = app.test_client()

    yield client

    # Add any application cleanup code here, after the yield


@pytest.fixture
def github_auth_header():
    """Header containing an ``Authorization`` key for GitHub-based auth.
    """
    encoded_creds = b64encode("{0}:{1}".format(TEST_USER, TEST_TOKEN).encode())
    return {
        'Authorization': 'Basic {0!s}'.format(encoded_creds.decode('utf-8'))
    }
