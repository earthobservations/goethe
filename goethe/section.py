# Goethe - Create Sphinx RST documents programmatically with Python
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
from collections import OrderedDict
from typing import TYPE_CHECKING, Optional, Union

from numpy.distutils.misc_util import as_list

from goethe.content import _CONTENT_TYPE, ContentFactory
from goethe.core import Core

if TYPE_CHECKING:
    from goethe.header import Header


class Section(Core):
    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        self._header = header

    @property
    def name(self):
        return self._name

    @property
    def content(self):
        return self._content

    def __init__(
        self, name: Union[str, "Header"], header: Optional[Union[str, "Header"]] = None, content: _CONTENT_TYPE = None
    ):
        super(Section, self).__init__()

        from goethe.header import Header
        from goethe.paragraph import Paragraph

        if not content:
            content = []
        content = [Paragraph(c) if type(c) == str else c for c in as_list(content)]

        self._name = name.header if type(name) == Header else name
        header = header or name
        self._header = header if type(header) == Header else Header(header)
        self._content = ContentFactory([Paragraph, Section])(content)

    def add_content(self, content) -> None:
        from goethe.paragraph import Paragraph

        content = [Paragraph(c) if type(c) == str else c for c in as_list(content)]
        self.content.add_content(content)

    def remove_content(self, cid: str):
        self.content.remove_content(cid)

    def clear(self):
        self.content.clear()

    def render(self) -> str:
        return f"{self.header.render()}\n\n{self.content.render()}"

    def to_dict(self) -> dict:
        return OrderedDict(
            {
                "name": self.name,
                "header": self.header.header,
                "text": self.render(),
            }
        )
