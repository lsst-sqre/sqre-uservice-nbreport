__all__ = ['healthcheck']

from . import api


@api.route("/")
def healthcheck():
    """Root endpoint used for Kubernetes health checks.
    """
    return "OK"
