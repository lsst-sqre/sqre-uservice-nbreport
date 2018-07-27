"""Exceptions used by the service to emit error responses.
"""

from apikit import BackendError


class ValidationError(BackendError):
    """Raised if there is an error validating a user request.

    Parameters
    ----------
    reason: `str`
        Reason for the exception
    status_code: `int`, optional
        Status code to be returned, defaults to 400.
    content: `str`, optional
        Textual content of the underlying error.
    """

    def __str__(self):
        return "ValidationError: {0:d} {1} [{2}]".format(
            self.status_code, self.reason, self.content)


class GitHubAuthenticationError(ValidationError):
    """Exception raised for GitHub authentication issues.
    """

    def __init__(self, reason=None, content=None):
        if reason is None:
            reason = ('Please authenticate using a GitHub username and '
                      'personal access token with Basic auth.')
        super().__init__(reason, status_code=401, content=content)

    def __str__(self):
        return "GitHubAuthenticationError: {0:d} {1} [{2}]".format(
            self.status_code, self.reason, self.content)


class GitHubAuthorizationError(ValidationError):
    """Exception raised if the user is not a member of the specified GitHub
    organization for authorization.
    """

    def __init__(self, reason=None, content=None):
        if reason is None:
            reason = ('You are not a member of the specified GitHub '
                      'organization for authorization.')
        super().__init__(reason, status_code=403, content=content)

    def __str__(self):
        return "GitHubAuthorizationError: {0:d} {1} [{2}]".format(
            self.status_code, self.reason, self.content)
