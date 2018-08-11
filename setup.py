#!/usr/bin/env python
"""Setuptools script.
"""
import os
import codecs
from setuptools import setup, find_packages

PACKAGENAME = 'sqre-uservice-nbreport'
DESCRIPTION = 'Publication service for LSST notebook-based reports'
AUTHOR = 'Jonathan Sick'
AUTHOR_EMAIL = 'jsick@lsst.org'
URL = 'https://github.com/sqre-lsst/uservice-nbreport'
LICENSE = 'MIT'


install_requires = [
    'sqre-apikit==0.1.2',
    'uWSGI==2.0.17',
    'Flask-HTTPAuth==3.2.4',
    'jupyter==1.0.0',  # provides nbformat, nbconvert and underlying infra
    'celery==4.2.1',
    'ltd-conveyor==0.4.0',
]

tests_require = [
    'pytest==3.6.3',
    'pytest-cov==2.5.1',
    'pytest-flake8==1.0.1',
    'responses==0.9.0'
]

extras_require = {
    'dev': tests_require
}

package_data = {'uservice_nbreport': [
    'uservice_nbreport/publish/templates/report-html/*.css',
    'uservice_nbreport/publish/templates/report-html/*.jinja',
]}

entry_points = {
    'nbconvert.exports': [
        'lsst-report-html '
        '= uservice_nbreport.publish.htmlexport:LsstHtmlReportExporter',
    ],
    'console_scripts': [
        'lsst-report-html '
        '= uservice_nbreport.publish.htmlexport:cli',
    ]
}


def local_read(filename):
    """Read a file into a string.
    """
    full_filename = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        filename)
    return codecs.open(full_filename, 'r', 'utf-8').read()


LONG_DESC = local_read('README.md')

setup(
    name=PACKAGENAME,
    description=DESCRIPTION,
    long_description=LONG_DESC,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='lsst',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    package_data=package_data,
    include_package_data=True,
    entry_points=entry_points,
)
