"""nbconvert preprocessor for building a document outline.
"""

__all__ = ('LsstOutlinePreprocessor',)

from copy import deepcopy

from nbconvert.preprocessors import Preprocessor
from nbconvert.filters.strings import _convert_header_id  # I know...


class LsstOutlinePreprocessor(Preprocessor):
    """Nbconvert preprocessor that generates a notebook section outline
    with computed anchor links.

    The outline is persisted in ``resources`` under the ``lsst_outline``
    field.
    """

    def preprocess(self, nb, resources):
        """Preprocess an entire notebook document.

        Parameters
        ----------
        nb : `nbformat.NotebookNode`
            Notebook being converted.
        resources : `dict`
            Additional resources used in the conversion process. This
            dictionary is available to Jinja templates.

        Returns
        -------
        nb : `nbformat.NotebookNode`
            Notebook being converted (unchanged).
        resources : `dict`
            Additional resources used in the conversion process. This
            dictionary is available to Jinja templates.
        """
        # cell_headers is a list of headers tuples
        # (int level, text, #anchor)
        cell_headers = []
        for cell in nb.cells:
            if cell.cell_type.lower() != 'markdown':
                continue

            cell_headers.extend(extract_markdown_headers(cell))

        # Now we need to convert this list of headers into a hierchical
        # structure to build the section outline.
        outline = build_outline_hierarchy(cell_headers)

        resources['lsst_outline_root'] = outline
        return nb, resources


def extract_markdown_headers(cell):
    """Extract the headers from a markdown cell.

    Parameters
    ----------
    cell : `nbformat.NotebookNode`
        A notebook cell, ``cell.cell_type == 'Markdown'``.

    Returns
    -------
    headers : list of dict
        List of headers, ordered as they occur in the cell's source. If the
        cell doesn't have any headers, the list is empty.

        Each list item is a dict with these fields:

        - ``level`` (`int`).
        - ``title``, like ``Report title`` (`str`).
        - ``anchor``, like ``#Report-title`` (`str`).
    """
    headers = []

    if cell.cell_type.lower() != 'markdown':
        return headers

    lines = cell.source.splitlines()
    for line in lines:
        if line.startswith('#'):
            parts = line.split()
            h = {
                'level': len(parts[0]),
                'title': ' '.join(parts[1:]),
            }
            h['anchor'] = ''.join(('#', _convert_header_id(h['title'])))
            headers.append(h)
    return headers


def build_outline_hierarchy(headers):
    headers = deepcopy(headers)

    root = RootNode()
    last = root
    while headers:
        header = headers.pop(0)
        if header['level'] == last.level:
            # Create sibling of last node
            node = OutlineNode(last.parent, header)
            last.parent.children.append(node)
        elif header['level'] > last.level:
            # create child of last node
            node = OutlineNode(last, header)
            last.children.append(node)
        else:
            # header['level'] < last.level
            parent = last.get_parent_of_level(header['level'] - 1)
            node = OutlineNode(parent, header)
            parent.children.append(node)
        last = node
    return root


class RootNode:

    children = []
    level = 0

    def __init__(self):
        pass

    def get_parent_of_level(self, level):
        return self


class OutlineNode:
    """Node in an header outline hierarchy."""

    @classmethod
    def from_headers(cls, headers, parent=None):
        next_header = headers.pop(0)

        return cls(parent, next_header['title'], next_header['anchor'],
                   remaining_header=headers)

    def __init__(self, parent, header_obj):
        self.parent = parent
        self.text = header_obj['title']
        self.anchor = header_obj['anchor']
        self.children = []

    @property
    def level(self):
        if self.parent is None:
            return 0
        else:
            return self.parent.level + 1

    def get_parent_of_level(self, level):
        if self.parent.level == level:
            return self.parent
        else:
            return self.parent.get_parent_of_level(level)
