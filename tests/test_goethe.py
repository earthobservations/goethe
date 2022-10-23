# Goethe - Create Sphinx RST documents programmatically with Python
# -*- coding: utf-8 -*-
# Copyright (C) 2022, Benjamin Gutzmann, earthobservations developers.
# Distributed under the MIT License. See LICENSE for more info.
from collections import OrderedDict
from pathlib import Path

import pytest

from goethe import DeepChapter, FlatChapter, Goethe, Section, TocTree

DEBUG = False
HERE = DEBUG and Path(__file__).parent


@pytest.fixture
def basic_goethe():
    goethe = Goethe(title="TestGoethe")

    goethe_toctree = goethe.add_content(TocTree())

    # Overview part / overview.rst
    overview = goethe_toctree.add_content(FlatChapter("overview"))

    introduction = overview.add_content(Section(name="FirstOverViewSection"))

    introduction.add_content("FirstOverViewSectionContent")

    # Deeper level part / index.rst
    deep_chapter = goethe_toctree.add_content(DeepChapter("deeper_level"))

    _ = deep_chapter.add_content(FlatChapter("introduction"))

    return goethe


def test_goethe_project_to_dict(basic_goethe):

    assert basic_goethe.to_dict() == OrderedDict(
        {
            "title": "TestGoethe",
            "path": ".",
            "content": [
                OrderedDict(
                    {
                        "name": None,
                        "config": None,
                        "render": ".. toctree:: \n\n   overview\n   deeper_level/index\n",
                        "content": [
                            OrderedDict(
                                {
                                    "name": "overview",
                                    "path": "overview.rst",
                                    "text": "overview\n########\n\nFirstOverViewSection\n####################\n\nFirstOverViewSectionContent",
                                    "content": [
                                        OrderedDict(
                                            {
                                                "name": "FirstOverViewSection",
                                                "header": "FirstOverViewSection",
                                                "text": "FirstOverViewSection\n####################\n\nFirstOverViewSectionContent",
                                            }
                                        )
                                    ],
                                }
                            ),
                            OrderedDict(
                                {
                                    "name": "deeper_level",
                                    "path": "deeper_level/index",
                                    "text": "deeper_level\n############\n\n.. toctree:: \n\n   introduction\n",
                                    "content": [
                                        OrderedDict(
                                            {
                                                "name": "introduction",
                                                "path": "deeper_level/introduction.rst",
                                                "text": "introduction\n############\n\n",
                                                "content": [],
                                            }
                                        )
                                    ],
                                }
                            ),
                        ],
                    }
                )
            ],
        }
    )


def test_goethe_project_write(basic_goethe, tmp_path):
    test_dir = HERE or tmp_path
    basic_goethe.to_rst(test_dir)


def test_debug():
    assert not DEBUG
