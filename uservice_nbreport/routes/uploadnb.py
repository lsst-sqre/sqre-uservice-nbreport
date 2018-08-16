"""Implementation for the POST /reports/<report>/instance/<id>/notebook
"""

__all__ = ('upload_notebook',)

from flask import request, jsonify, url_for

from . import api
from ..auth import github_token_auth, requires_github_org_membership, ltd_login
from ..exceptions import ValidationError
from ..tasks import publish_instance


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

    nb_data = request.data.decode('utf-8')

    task = publish_instance.apply_async(args=[nb_data, report, instance_id])

    url = url_for('api.get_queue_item', id=task.id, _external=True)

    data = {
        'queue_url': url
    }

    return jsonify(data), 202
