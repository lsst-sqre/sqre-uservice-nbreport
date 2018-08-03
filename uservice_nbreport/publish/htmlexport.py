"""Notebook HTML export with nbconvert, customized for LSST reports.
"""

__all__ = ('LsstHtmlReportExporter',)

from pathlib import Path

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

    # @default('default_template_path')
    # def _default_template_path_default(self):

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
