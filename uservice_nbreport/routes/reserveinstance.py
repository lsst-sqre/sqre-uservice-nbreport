"""Endpoint for reserving an instance number.

Reserving an instance is done by creating an edition for the given product.
"""

__all__ = ('reserve_instance',)

from urllib.parse import urljoin

from apikit import BackendError
from flask import g, request, jsonify, current_app
import requests

from . import api
from ..auth import github_token_auth, requires_github_org_membership, ltd_login
from ..exceptions import ValidationError


@api.route('/reports/<report>/instances/', methods=['POST'])
@github_token_auth.login_required
@requires_github_org_membership()
@ltd_login()
def reserve_instance(report):
    """Reserve a new edition for this report.
    """
    request_data = request.json

    try:
        product = request_data['product']
    except KeyError as e:
        raise ValidationError('Invalid request: missing ' + e.args[0])

    edition_request_data = {
        'autoincrement': True,
        'mode': 'manual'
    }
    new_edition_endpoint = urljoin(
        current_app.config['KEEPER_URL'],
        '/products/{product}/editions/'.format(product=product))
    response = requests.post(
        new_edition_endpoint,
        json=edition_request_data,
        auth=(g.ltd_user, g.ltd_token)
    )
    if response.status_code >= 300:
        raise BackendError(
            "Unexcepted error calling LSST the Docs's "
            "POST /products/<product>/editions/ endpoint",
            status_code=500,
            content=str(response.json()))

    edition_url = response.headers['location']
    response = requests.get(edition_url)
    if response.status_code >= 300:
        raise BackendError(
            "Unexcepted error calling LSST the Docs's "
            "GET {} endpoint".format(edition_url),
            status_code=500,
            content=str(response.json()))

    instance_id = response.json()['slug']

    return jsonify({'instance_id': instance_id}), 201
