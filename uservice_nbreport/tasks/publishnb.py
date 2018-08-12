"""Celery task for publishing a notebook report instance.
"""

__all__ = ('publish_instance',)

from pathlib import Path
import shutil
import tempfile
from urllib.parse import urljoin

from flask import current_app
from celery.utils.log import get_task_logger
from ltdconveyor.keeper.build import register_build, confirm_build
from ltdconveyor.keeper.login import get_keeper_token
from ltdconveyor.s3 import upload_dir
import requests
import nbformat

from ..celery import celery_app
from ..publish.htmlexport import LsstHtmlReportExporter

logger = get_task_logger(__name__)


@celery_app.task(bind=True)
def publish_instance(self, nb_data, ltd_product, instance_id):
    """Publish a notebook instance (Celery task).

    Parameters
    ----------
    nb_data : `str`
        Notebook document, serialized as a string.
    ltd_product : `str`
        Slug of the LTD Product resource corresponding to the report.
    instance_id : `str`
        Identifier of the instance, usually an integer as a string. This is
        the slug of the LTD Edition corresponding to the report instance.
    """
    ltd_token = get_keeper_token(
        current_app.config['KEEPER_URL'],
        current_app.config['KEEPER_USERNAME'],
        current_app.config['KEEPER_PASSWORD'],
    )

    kwargs = {
        'keeper_url': current_app.config['KEEPER_URL'],
        'ltd_token': ltd_token,
        'ltd_product': ltd_product,
        'instance_id': instance_id,
        'aws_id': current_app.config['KEEPER_AWS_ID'],
        'aws_secret': current_app.config['KEEPER_AWS_SECRET'],
    }

    nb = nbformat.reads(nb_data, as_version=4)

    with tempfile.TemporaryDirectory() as tempdir:
        work_dir = Path(tempdir)
        run_publish_instance(nb=nb, work_dir=work_dir, **kwargs)


def run_publish_instance(*, nb, work_dir, keeper_url, ltd_token, ltd_product,
                         instance_id, aws_id, aws_secret):
    """Publish a notebook instance.

    This is a standalone function typically called by the `publish_instance`
    task.

    Parameters
    ----------
    nb : `nbformat.NotebookNode`
        The notebook document.
    work_dir : `pathlib.Path`
        Directory where the HTML and other website assets are staged for
        upload.
    """
    # Export report notebook to HTML
    create_html(nb, work_dir)

    # Upload to LTD
    upload_html(work_dir=work_dir, keeper_url=keeper_url,
                ltd_token=ltd_token, ltd_product=ltd_product,
                instance_id=instance_id, aws_id=aws_id, aws_secret=aws_secret)


def create_html(nb, work_dir):
    """Convert the notebook into an HTML LSST report.

    Parameters
    ----------
    nb : `nbformat.NotebookNode`
        The notebook document.
    work_dir : `pathlib.Path`
        Directory where the HTML and other website assets are staged for
        upload.
    keeper_url : `str`
        Base URL of the LTD Keeper API.
    ltd_token : `str`
        Token for the LTD Keeper API.
    ltd_product : `str`
        Slug of the LTD Product resource corresponding to the report.
    instance_id : `str`
        Identifier of the instance, usually an integer as a string. This is
        the slug of the LTD Edition corresponding to the report instance.
    aws_id : `str`
        AWS key identifier. Used for uploading files to LSST the Docs's
        S3 bucket.
    aws_secret : `str`
        AWS secret key. Used for uploading files to LSST the Docs's S3 bucket.
    """
    exporter = LsstHtmlReportExporter()
    body, resources = exporter.from_notebook_node(nb)

    # Write the HTML to the integration directory
    (work_dir / 'index.html').write_text(body)

    for asset_path in exporter.asset_paths:
        dest = work_dir / asset_path.name
        shutil.copy(asset_path, dest)


def upload_html(*, work_dir, keeper_url, ltd_token, ltd_product, instance_id,
                aws_id, aws_secret):
    """Upload the build HTML site for the notebook report instance.

    Parameters
    ----------
    work_dir : `pathlib.Path`
        Directory where the HTML and other website assets are staged for
        upload.
    keeper_url : `str`
        Base URL of the LTD Keeper API.
    ltd_token : `str`
        Token for the LTD Keeper API.
    ltd_product : `str`
        Slug of the LTD Product resource corresponding to the report.
    instance_id : `str`
        Identifier of the instance, usually an integer as a string. This is
        the slug of the LTD Edition corresponding to the report instance.
    aws_id : `str`
        AWS key identifier. Used for uploading files to LSST the Docs's
        S3 bucket.
    aws_secret : `str`
        AWS secret key. Used for uploading files to LSST the Docs's S3 bucket.
    """
    build_resource = register_build(keeper_url, ltd_token, ltd_product,
                                    [instance_id])

    # This cache_control is appropriate for builds since they're immutable.
    # The LTD Keeper server changes the cache settings when copying the build
    # over to be a mutable edition.
    upload_dir(
        build_resource['bucket_name'],
        build_resource['bucket_root_dir'],
        str(work_dir),
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_secret,
        surrogate_key=build_resource['surrogate_key'],
        cache_control='max-age=31536000',
        surrogate_control=None,
        upload_dir_redirect_objects=True)

    confirm_build(build_resource['self_url'], ltd_token)

    edition_url = get_edition_url(keeper_url=keeper_url,
                                  ltd_token=ltd_token,
                                  ltd_product=ltd_product,
                                  instance_id=instance_id)

    # Update the edition to use this build.
    update_edition(ltd_token=ltd_token,
                   edition_url=edition_url,
                   build_url=build_resource['self_url'])


def get_edition_url(*, keeper_url, ltd_token, ltd_product, instance_id):
    """Find the API URL of the edition corresponding to the instance_id.

    This is currently a bit of a hack since LTD Keeper doesn't have a way of
    directly obtaining an edition based on its slug (instance_id).

    Parameters
    ----------
    keeper_url : `str`
        Base URL of the LTD Keeper API.
    ltd_token : `str`
        Token for the LTD Keeper API.
    ltd_product : `str`
        Slug of the LTD Product resource corresponding to the report.
    instance_id : `str`
        Identifier of the instance, usually an integer as a string. This is
        the slug of the LTD Edition corresponding to the report instance.

    Returns
    -------
    edition_url : `str`
        URL of the edition in the LTD Keeper API (not the front-end website
        URL).
    """
    root_url = urljoin(
        keeper_url, '/products/{0}/editions/'.format(ltd_product))
    response = requests.get(
        root_url, auth=(ltd_token, ''))
    response.raise_for_status()
    edition_urls = response.json()['editions']

    for edition_url in reversed(edition_urls):
        response = requests.get(edition_url, auth=(ltd_token, ''))
        response.raise_for_status()
        if response.json()['slug'] == instance_id:
            return edition_url

    raise RuntimeError(
        'Could not identify the URL for an edition with slug={0}'.format(
            instance_id))


def update_edition(*, ltd_token, edition_url, build_url):
    """Update the Edition resource to point to a new Build.

    Parameters
    ----------
    ltd_token : `str`
        Token for the LTD Keeper API.
    edition_url : `str`
        URL of the edition in the LTD Keeper API (not the front-end website
        URL).
    build_url : `str`
        URL of the build in the LTD Keeper API.
    """
    data = {
        'build_url': build_url
    }
    response = requests.patch(
        edition_url,
        auth=(ltd_token, ''),
        json=data
    )
    response.raise_for_status()
