"""``/login`` endpoint for testing logins.
"""

__all__ = ('login',)

from flask import g, jsonify

from . import api
from ..auth import github_token_auth, requires_github_org_membership


@api.route('/login', methods=['POST'])
@github_token_auth.login_required
@requires_github_org_membership()
def login():
    """Test logging into the service with GitHub credentials for both
    authentication and organization-based authorization.
    """
    print('Logged in {}'.format(g.github_user))
    return jsonify({}), 200
