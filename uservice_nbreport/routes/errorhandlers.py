"""Exception handling to generate HTTP responses.
"""

__all__ = ('handle_invalid_usage',)

from apikit import BackendError
from flask import jsonify
from structlog import get_logger

from . import api


@api.errorhandler(BackendError)
def handle_invalid_usage(error):
    """Custom error handler.
    """
    logger = get_logger()
    errdict = error.to_dict()
    logger.error(errdict)
    response = jsonify(errdict)
    response.status_code = error.status_code
    return response
