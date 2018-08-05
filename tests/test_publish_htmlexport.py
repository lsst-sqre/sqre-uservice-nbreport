"""Tests for the uservice_nbreport.publish.htmlexport module.
"""

from pathlib import Path

from uservice_nbreport.publish.htmlexport import build_site_from_filename


def test_basic_export(tmpdir):
    """Basic test of LsstHtmlReportExporter with a test notebook.
    """
    path = Path(__file__).parent / 'notebooks/basic.ipynb'
    assert path.exists()

    build_site_from_filename(path, tmpdir)

    assert (tmpdir / 'index.html').exists()
    assert (tmpdir / 'app.css').exists()
