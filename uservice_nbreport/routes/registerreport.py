"""Implementation for the POST /nbreport/reports/ endpoint to register a new
report.
"""

__all__ = ('register_report',)

from urllib.parse import urljoin

from apikit import BackendError
from flask import g, jsonify, request, current_app
import requests

from . import api
from ..auth import github_token_auth, requires_github_org_membership, ltd_login
from ..exceptions import ValidationError


@api.route('/reports/', methods=['POST'])
@github_token_auth.login_required
@requires_github_org_membership()
@ltd_login()
def register_report():
    """Register a new report by creating a report product on LSST the Docs.
    """
    request_data = request.json

    try:
        handle = request_data['handle']
        title = request_data['title']
        git_repo = request_data['git_repo']
    except KeyError as e:
        raise ValidationError('Invalid request: missing ' + e.args[0])

    product_data = {
        'bucket_name': 'lsst-the-docs',
        'doc_repo': git_repo,
        'root_domain': 'lsst.io',
        'root_fastly_domain': "n.global-ssl.fastly.net",
        'slug': handle.lower(),
        'title': title,
        'main_mode': 'manual'
    }
    product_response = requests.post(
        urljoin(current_app.config['KEEPER_URL'], '/products/'),
        json=product_data,
        auth=(g.ltd_token, '')
    )
    if product_response.status_code >= 300:
        raise BackendError(
            "Unexcepted error calling LSST the Docs's POST /products/ "
            "endpoint",
            status_code=500,
            content=str(product_response.json()))
    product_url = product_response.headers['Location']

    # Get more data about the product
    product_response = requests.get(
        product_url,
        auth=(g.ltd_token, '')
    )
    if product_response.status_code >= 300:
        raise BackendError(
            "Unexcepted error calling LSST the Docs's GET {0!s} "
            "endpoint".format(product_url),
            status_code=500,
            content=str(product_response.json()))
    product_resource = product_response.json()

    response_data = {
        'product': product_resource['slug'],
        'published_url': product_resource['published_url'],
        'product_url': product_resource['self_url']
    }
    return jsonify(response_data), 201
