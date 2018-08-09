"""Access the application version.
"""

__all__ = ('get_version',)

from pkg_resources import get_distribution, DistributionNotFound


def get_version():
    try:
        return get_distribution('sqre-uservice-nbreport').version
    except DistributionNotFound:
        # Package is not installed
        return '0.0.0'
