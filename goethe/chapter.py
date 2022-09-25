# Goethe - Create Sphinx RST documents programmatically with Python
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
import pathlib
from collections import OrderedDict
from pathlib import Path

from numpy.distutils.misc_util import as_list

from goethe.content import ContentFactory
from goethe.core import Core
from goethe.header import Header
from goethe.toctree import TocTree


class FlatChapter(Core):
    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, folder):
        folder = Path(folder)
        self._folder = folder
        for c in self.content:
            c.folder = folder

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._name

    @property
    def header(self):
        return Header(self.title)

    @property
    def toc_name(self) -> str:
        return self.name

    @property
    def filename(self):
        return f"{self.name}.rst"

    @property
    def path(self):
        return self._folder and self._folder / self.filename

    @property
    def content(self):
        return self._content

    def __init__(self, name: str, content=None):
        super(FlatChapter, self).__init__()

        from goethe.paragraph import Paragraph
        from goethe.section import Section

        if not content:
            content = []
        content = [Paragraph(c) if type(c) == str else c for c in as_list(content)]

        self._name = name
        self._content = ContentFactory([Paragraph, Section])(content)
        self._folder = None

    def add_content(self, content):
        self.content.add_content(content)
        return content

    def remove_content(self, cid: str):
        self.content.remove_content(cid)

    def clear(self):
        self.content.clear()

    def render(self) -> str:
        return f"{self.header.render()}\n\n{self.content.render()}"

    def to_dict(self) -> dict:
        return OrderedDict(
            {
                "name": self._name,
                "path": str(self.path),
                "text": self.render(),
                "content": [c.to_dict() for c in self.content],
            }
        )

    def to_rst(self, path: pathlib.Path) -> None:
        fpath = path
        if path.is_dir():
            fpath = path / self.filename
            fpath.unlink(missing_ok=True)
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(self.render())


class DeepChapter(Core):
    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._name

    @property
    def header(self):
        return Header(self.title)

    @property
    def filename(self) -> str:
        return f"{self.name}/index.rst"

    @property
    def toc_name(self) -> str:
        return f"{self.name}/index"

    @property
    def path(self):
        return self._folder and self._folder / self.toc_name

    @property
    def folder(self):
        return self._folder and self._folder / self.name

    @folder.setter
    def folder(self, folder):
        folder = Path(folder)
        self._folder = folder
        for c in self.content:
            c.folder = folder

    @property
    def content(self):
        return self._content

    def __init__(self, name: str, content=None):
        super(DeepChapter, self).__init__()

        self._name = name
        self._content = ContentFactory([FlatChapter, DeepChapter])(content)
        self._folder = None

    def add_content(self, content):
        content._folder = self.folder
        self.content.add_content(content)

    def remove_content(self, cid: str):
        self.content.remove_content(cid)

    def clear(self):
        self.content.clear()

    def render(self) -> str:
        return f"{self.header.render()}\n\n{TocTree(self.content).render()}"

    def to_dict(self):
        return OrderedDict(
            {
                "name": self.name,
                "path": str(self.path),
                "text": self.render(),
                "content": [c.to_dict() for c in self.content],
            }
        )

    def to_rst(self, path: pathlib.Path):
        fpath = path
        if path.is_dir():
            fpath = path / self.filename
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(self.render())

        for c in self.content:
            c.to_rst(fpath.parent)
