"""Tests for the POST /reports/<report>/instances/ endpoint.
"""

import json

import responses
from werkzeug.http import parse_authorization_header
from flask import current_app


@responses.activate
def test_reserve_instance(client, github_auth_header):
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
    # Initial reservation of the edition with LTD Keeper
    responses.add(
        responses.POST,
        'https://keeper.lsst.codes/products/testr-000/editions/',
        status=201,
        json={},
        headers={'Location': 'https://keeper.lsst.codes/editions/1'}
    )
    # Request to obtain the full edition resource
    responses.add(
        responses.GET,
        'https://keeper.lsst.codes/editions/1',
        status=200,
        json={'slug': '1'},
        headers={'Location': 'https://keeper.lsst.codes/editions/1'}
    )

    with client:
        headers = dict(github_auth_header)
        headers['Content-Type'] = 'application/json'
        response = client.post(
            '/nbreport/reports/testr-000/instances/',
            headers=headers,
        )
        assert response.status_code == 201

        response_data = json.loads(response.data.decode('utf-8'))
        assert response_data['instance_id'] == '1'

        # Test the POST /products/<slug>/editions/ request
        post_editions_request_data = json.loads(
            responses.calls[3].request.body.decode('utf-8'))
        assert post_editions_request_data['autoincrement'] is True
        assert post_editions_request_data['mode'] == 'manual'
        # Test authorization header
        auth = parse_authorization_header(
            responses.calls[3].request.headers['Authorization'])
        assert auth is not None
        assert auth.username == current_app.config['KEEPER_USERNAME']
        assert auth.password == 'ltdtoken'
