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

    KEEPER_URL = os.getenv('KEEPER_URL', 'https://keeper.lsst.codes')
    """URL of the LSST the Docs API server.

    Set via ``$KEEPER_URL``.
    """

    KEEPER_USERNAME = os.getenv('KEEPER_USERNAME')
    """Username of of the LTD Keeper account this app uses on behalf of the
    user.

    Set via ``$KEEPER_USERNAME``.
    """

    KEEPER_PASSWORD = os.getenv('KEEPER_PASSWORD')
    """Password of of the LTD Keeper account this app uses on behalf of the
    user.

    Set via ``$KEEPER_PASSWORD``.
    """

    CELERY_RESULT_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    """URI for the celery result store (Redis).
    """

    CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    """URI for the celery task broker (Redis).
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

    KEEPER_USERNAME = 'ltduser'

    KEEPER_PASSWORD = 'ltdpassword'


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
