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


class TestingConfig(ConfigurationBase):
    """Configuration defaults for testing (with pytest).
    """

    PROFILE = 'test'
    """Name of this configuration profile.
    """

    TESTING = True
    """Enable Flask's testing mode.
    """


class ProductionConfig(ConfigurationBase):
    """Configuration defaults for production.
    """

    PROFILE = 'production'
    """Name of this configuration profile.
    """


config_profiles = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
}
