"""Tests for the POST /reports/ endpoint.
"""

import json

from flask import g, current_app
import responses
from werkzeug.http import parse_authorization_header


@responses.activate
def test_register_report(client, github_auth_header):
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
    responses.add(
        responses.GET,
        'https://keeper.lsst.codes/token',
        status=200,
        json={'token': 'ltdtoken'}
    )
    # Initial product registration
    responses.add(
        responses.POST,
        'https://keeper.lsst.codes/products/',
        status=201,
        json={},
        headers={'Location': 'https://keeper.lsst.codes/products/testr-000'}
    )
    # Getting info about the product resource
    responses.add(
        responses.GET,
        'https://keeper.lsst.codes/products/testr-000',
        status=200,
        json={
            'slug': 'testr-000',
            'published_url': 'https://testr-000.lsst.io',
            'self_url': 'https://keeper.lsst.codes/products/testr-000'}
    )

    with client:
        headers = dict(github_auth_header)
        headers['Content-Type'] = 'application/json'
        response = client.post(
            '/nbreport/reports/',
            headers=headers,
            data=json.dumps({
                'handle': 'TESTR-000',
                'title': 'Demo report',
                'git_repo': 'https://github.com/lsst-sqre/nbreport'
            })
        )
        assert response.status_code == 201
        response_data = json.loads(response.data.decode('utf-8'))

        assert g.ltd_user == current_app.config['KEEPER_USERNAME']
        assert g.ltd_token == 'ltdtoken'

        assert response_data['product'] == 'testr-000'

        # Test the call to POST keeper.lsst.codes/products/
        post_products_request_data = json.loads(
            responses.calls[3].request.body.decode('utf-8'))
        assert post_products_request_data['slug'] == 'testr-000'
        assert post_products_request_data['title'] == 'Demo report'
        assert post_products_request_data['main_mode'] == 'manual'
        # Test authorization header
        auth = parse_authorization_header(
            responses.calls[3].request.headers['Authorization'])
        assert auth is not None
        assert auth.username == 'ltdtoken'
        assert auth.password == ''

        # Test the call to GET /products/testr-000
        assert responses.calls[4].request.url \
            == 'https://keeper.lsst.codes/products/testr-000'
