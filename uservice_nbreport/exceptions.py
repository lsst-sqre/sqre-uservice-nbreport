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
