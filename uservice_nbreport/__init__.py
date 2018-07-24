#!/usr/bin/env python
"""SQuaRE nbreport microservice (api.lsst.codes-compliant).
"""
from .server import server, standalone
__all__ = ["server", "standalone"]
