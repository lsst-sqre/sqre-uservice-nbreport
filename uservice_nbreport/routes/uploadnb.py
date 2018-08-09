"""Implementation for the POST /reports/<report>/instance/<id>/notebook
"""

__all__ = ('upload_notebook',)

# from urllib.parse import urljoin

# from flask import g, request, jsonify, current_app
from flask import request, jsonify
# import requests
import nbformat

from . import api
from ..auth import github_token_auth, requires_github_org_membership, ltd_login
from ..exceptions import ValidationError


@api.route('/reports/<report>/instances/<instance_id>/notebook',
           methods=['POST'])
@github_token_auth.login_required
@requires_github_org_membership()
@ltd_login()
def upload_notebook(report, instance_id):
    """Upload a notebook file corresponding to an instance of a report
    for publication.
    """
    # Check mimetype: application/x-ipynb+json
    # https://jupyter.readthedocs.io/en/latest/reference/mimetype.html
    if request.mimetype != 'application/x-ipynb+json':
        raise ValidationError(
            'Content-Type must be application/x-ipynb+json (an ipynb '
            'notebook file). See '
            'https://jupyter.readthedocs.io/en/latest/reference/mimetype.html '
            'for more information',
            status_code=400,
            content='Sent mimetype {}'.format(request.mimetype))

    notebook_data = request.data.decode('utf-8')
    nb = nbformat.reads(notebook_data, as_version=4)
    print(nb)

    # TODO pass the nb, or just notebook_data, on to the asynchronous
    # task service.

    return jsonify({}), 202
