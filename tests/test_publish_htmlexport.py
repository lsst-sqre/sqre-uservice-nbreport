"""Tests for the uservice_nbreport.publish.htmlexport module.
"""

from pathlib import Path

from uservice_nbreport.publish.htmlexport import LsstHtmlReportExporter


def test_basic_export():
    """Basic test of LsstHtmlReportExporter with a synthesized notebook.
    """
    path = Path(__file__).parent / 'notebooks/basic.ipynb'
    assert path.exists()

    exporter = LsstHtmlReportExporter()

    body, resources = exporter.from_filename(str(path))
    assert body is not None
