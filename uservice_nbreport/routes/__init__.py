"""Application routes blueprint.
"""

__all__ = ('api',)

from flask import Blueprint

# Create api before importing modules because they need it.
api = Blueprint('api', __name__)

from .errorhandlers import *
from .root import *
from .login import *
