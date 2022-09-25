# Goethe - Create Sphinx RST documents programmatically with Python
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
import pathlib
from collections import OrderedDict
from pathlib import Path
from typing import TYPE_CHECKING, Union

from goethe.core import Core

if TYPE_CHECKING:
    from goethe import TocTree

CWD = Path(".").resolve()


class Goethe(Core):
    """RST project"""

    filename = "index.rst"

    def __init__(self, title: str, path: Union[str, Path] = CWD):
        super(Goethe, self).__init__()
        self.title = title
        self.path = Path(path)
        self.content = []

    def add_content(self, content) -> "TocTree":
        content.folder = self.path
        self.content.append(content)
        return content

    def to_dict(self) -> dict:
        return OrderedDict(
            {
                "title": self.title,
                "path": self.path and str(self.path) or None,
                "content": [c.to_dict() for c in self.content],
            }
        )

    def to_json(self) -> str:
        pass

    def render(self) -> str:
        content = f"{self.title}\n\n"
        for c in self.content:
            content += c.render()
        return content

    def to_rst(self, path: pathlib.Path):
        path.mkdir(parents=True, exist_ok=True)
        fpath = path / self.filename
        if fpath.exists():
            fpath.unlink(True)
        fpath.write_text(self.render())

        for c in self.content:
            c.to_rst(path)
