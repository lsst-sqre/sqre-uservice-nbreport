"""Notebook HTML export with nbconvert, customized for LSST reports.
"""

__all__ = ('LsstHtmlReportExporter', 'build_site_from_filename', 'cli')

from pathlib import Path
import shutil

import click
from nbconvert.exporters.html import HTMLExporter
from traitlets import default, Unicode


class LsstHtmlReportExporter(HTMLExporter):
    """nbconvert exporter to HTML, customized for LSST notebook-based reports.
    """

    anchor_link_text = Unicode(
        '#',
        help="The text used as the text for anchor links.").tag(config=True)

    @property
    def export_from_notebook(self):
        """Name of the notebook in the File -> Download as menu (`str`).
        """
        # If None, then this exporter won't be visible from the
        # File -> Download menu
        return 'LSST report (HTML)'

    @property
    def template_path(self):
        """Paths to the directories containing templates for the HTML reports.
        """
        path = Path(__file__).parent / 'templates/report-html'
        # add our custom template path to the base template search paths.
        return super().template_path + [str(path)]

    @default('template_file')
    def _template_file_default(self):
        """Name of the default template file.
        """
        return 'report.jinja'

    @property
    def asset_paths(self):
        """Paths to static assets that must also be shipped with the site.
        """
        css_path = Path(__file__).parent / 'templates/report-html/app.css'
        return [css_path]


def build_site_from_filename(notebook_path, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exporter = LsstHtmlReportExporter()
    body, resources = exporter.from_filename(str(notebook_path))

    (output_dir / 'index.html').write_text(body)

    for asset_path in exporter.asset_paths:
        dest = output_dir / asset_path.name
        shutil.copy(asset_path, dest)
        # NOTE: assumes all asset paths should reside in same directory
        # as index.html

    # FIXME write out the resources too.


@click.command()
@click.argument(
    'notebook',
    default=Path(__file__).parent / '../../tests/notebooks/basic.ipynb')
@click.argument(
    'site_dir',
    default=Path('test-sites/basic'))
def cli(notebook, site_dir):
    """Build the HTML site for a notebook using the LSST report notebook
    to HTML converter.
    """
    notebook = Path(notebook)
    site_dir = Path(site_dir)
    build_site_from_filename(notebook, site_dir)
