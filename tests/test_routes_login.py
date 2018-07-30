"""Test GET /login and hence the authentication and authorization code.
"""

from flask import g
import responses

from conftest import TEST_USER, TEST_TOKEN


@responses.activate
def test_login(client, github_auth_header):
    """Test a successful log in."""
    responses.add(
        responses.GET,
        'https://api.github.com/user',
        status=200,
        json={
            'login': 'testuser'
        }
    )
    responses.add(
        responses.GET,
        'https://api.github.com/user/orgs',
        status=200,
        json=[
            {
                'login': 'lsst'
            }
        ]
    )

    with client:
        response = client.post(
            '/nbreport/login',
            headers=github_auth_header
        )
        responses.calls[0].request.url == 'https://api.github.com/user'
        responses.calls[1].request.url == 'https://api.github.com/user/orgs'
        assert response.status_code == 200

        assert g.github_user == TEST_USER
        assert g.github_token == TEST_TOKEN


@responses.activate
def test_failed_authentication(client, github_auth_header):
    """Test failed authentication."""
    responses.add(
        responses.GET,
        'https://api.github.com/user',
        status=401,
        json={}
    )
    responses.add(
        responses.GET,
        'https://api.github.com/user/orgs',
        status=200,
        json=[
            {
                'login': 'lsst'
            }
        ]
    )

    with client:
        response = client.post(
            '/nbreport/login',
            headers=github_auth_header
        )
        assert response.status_code == 401
        responses.calls[0].request.url == 'https://api.github.com/user'

        # GitHub user data was never persisted
        assert hasattr(g, 'github_user') is False
        assert hasattr(g, 'github_token') is False


@responses.activate
def test_failed_authorization(client, github_auth_header):
    """Test failed meaning the user is not in the right GitHub org."""
    responses.add(
        responses.GET,
        'https://api.github.com/user',
        status=200,
        json={
            'login': 'testuser'
        }
    )
    responses.add(
        responses.GET,
        'https://api.github.com/user/orgs',
        status=200,
        json=[
            {
                'login': 'lsst-other'
            },
            {
                'login': 'random'
            }
        ]
    )

    with client:
        response = client.post(
            '/nbreport/login',
            headers=github_auth_header
        )
        responses.calls[0].request.url == 'https://api.github.com/user'
        responses.calls[1].request.url == 'https://api.github.com/user/orgs'
        assert response.status_code == 403

        # Authentication data exists, still
        assert g.github_user == TEST_USER
        assert g.github_token == TEST_TOKEN
