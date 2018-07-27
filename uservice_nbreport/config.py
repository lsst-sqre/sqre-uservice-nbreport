"""Application configuration facilities.
"""

__all__ = ('config_profiles',)

import abc
import os


class ConfigurationBase(metaclass=abc.ABCMeta):
    """Configuration base class.
    """

    DEBUG = False
    """Flask's DEBUG mode.
    """

    AUTHORIZED_GITHUB_ORG = os.getenv('AUTH_GITHUB_ORG', 'lsst')
    """Name of the GitHub organization a user must be a member of to be
    authorized.

    Default: ``lsst``

    Set via ``$AUTH_GITHUB_ORG``.
    """


class DevelopmentConfig(ConfigurationBase):
    """Configuration defaults for development.
    """

    PROFILE = 'dev'
    """Name of this configuration profile.
    """

    DEBUG = True
    """Flask's DEBUG mode is always active during development.
    """


config_profiles = {
    'dev': DevelopmentConfig
}
