"""Tests for the ``uservice_nbreport.publish.outline`` module.
"""

import nbformat

from uservice_nbreport.publish.outline import (
    extract_markdown_headers,
    build_outline_hierarchy)


def test_extract_markdown_headers():
    source = (
        '# Report title\n'
        '\n'
        'This is a regular paragraph of #awesome.\n'
        '\n'
        '## Subsection\n'
        '\n'
        'More text.\n'
        '\n'
        '### Sub-subsection\n'
        '\n'
        'Yup.\n'
    )
    expected = [
        dict(level=1, title='Report title', anchor='#Report-title'),
        dict(level=2, title='Subsection', anchor='#Subsection'),
        dict(level=3, title='Sub-subsection', anchor='#Sub-subsection'),
    ]
    cell = nbformat.v4.new_markdown_cell(source=source)
    assert extract_markdown_headers(cell) == expected


def test_build_outline_hierarchy():
    headers = [
        dict(level=1,
             title='Report title',
             anchor='#Report-title'),
        dict(level=2,
             title='Subsection',
             anchor='#Subsection'),
        dict(level=3,
             title='Sub-subsection',
             anchor='#Sub-subsection'),
        dict(level=2,
             title='Sibling subsection',
             anchor='#Sibling-subsection'),
    ]

    outline = build_outline_hierarchy(headers)

    h1 = outline.children[0]
    assert h1.text == 'Report title'
    assert len(h1.children) == 2

    assert h1.children[0].text == 'Subsection'
    assert h1.children[1].text == 'Sibling subsection'

    assert h1.children[0].children[0].text == 'Sub-subsection'
