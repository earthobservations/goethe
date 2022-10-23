# Goethe - Create Sphinx RST documents programmatically with Python
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Union

from goethe.content import ContentFactory
from goethe.core import Core

if TYPE_CHECKING:
    from goethe.chapter import DeepChapter, FlatChapter

_CONTENT_TYPE = Optional[Union["FlatChapter", "DeepChapter", List[Union["FlatChapter", "DeepChapter"]]]]


class TocTree(Core):
    _indent = "   "

    @property
    def path(self):
        return self._path

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, folder):
        self._folder = Path(folder)
        for c in self.content:
            c.folder = folder

    @property
    def content(self):
        return self._content

    @property
    def name(self):
        return self._name

    @property
    def config(self):
        return self._config

    def __init__(
        self,
        content: _CONTENT_TYPE = None,
        name: Optional[str] = None,
        config: Optional[dict] = None,
    ):
        super(TocTree, self).__init__()

        from goethe.chapter import DeepChapter, FlatChapter

        self._content = ContentFactory([FlatChapter, DeepChapter])(content)
        self._name = name
        self._config = config
        self._folder = None

    def add_content(self, content):
        content.folder = self.folder
        self.content.add_content(content)
        return content

    def to_dict(self):
        return OrderedDict(
            {
                "name": self.name,
                "config": self.config,
                "render": self.render(),
                "content": [c.to_dict() for c in self.content],
            }
        )

    def render(self):
        toctree = f".. toctree:: {self.name or ''}\n"

        if self.config:
            for key, value in self.config.items():
                toctree += f"{self._indent}:{key}: {value}\n"

        toctree += "\n"

        for section in self.content:
            toctree += f"{self._indent}{section.toc_name}\n"

        return toctree

    def to_rst(self, path: Path):
        for c in self.content:
            c.to_rst(path)
