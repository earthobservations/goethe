goethe
######

Create RST documents programmatically with Python

.. image:: https://github.com/earthobservations/goethe/workflows/Tests/badge.svg
   :target: https://github.com/earthobservations/goethe/actions?workflow=Tests
   :alt: CI: Overall outcome
.. image:: https://codecov.io/gh/earthobservations/goethe/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/earthobservations/goethe
   :alt: CI: Code coverage
.. image:: https://img.shields.io/pypi/v/goethe.svg
   :target: https://pypi.org/project/goethe/
   :alt: PyPI version
.. image:: https://img.shields.io/pypi/status/goethe.svg
   :target: https://pypi.python.org/pypi/goethe/
   :alt: Project status (alpha, beta, stable)
.. image:: https://pepy.tech/badge/goethe/month
   :target: https://pepy.tech/project/goethe
   :alt: PyPI downloads
.. image:: https://img.shields.io/github/license/earthobservations/goethe
   :target: https://github.com/earthobservations/goethe/blob/main/LICENSE
   :alt: Project license
.. image:: https://img.shields.io/pypi/pyversions/goethe.svg
   :target: https://pypi.python.org/pypi/goethe/
   :alt: Python version compatibility
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Documentation: Black

----

WARNING: THIS PROJECT IS CURRENTLY IN ALPHA STAGE. DON'T USE IN PRODUCTION!

----

Introduction
************

Goethe gives you the opportunity to create your individual RST project in Python

1. **programmatically** - write your project as Python script in OOP style, place variables where ever you want
2. **dynamically** - render the project to dict, json or actual files and even PDF

Setup
*****

Via Pip:

.. code-block:: bash

    pip install goethe

Via Github (latest):

.. code-block:: bash

    pip install git+https://github.com/earthobservations/goethe

Structure
*********

Goethe uses 3 main levels of abstraction:

- Goethe - initialize an RST project with a Goethe
- FlatChapter - add a chapter based on one file at the same level as the Goethe
- DeepChapter - add a chapter based on a folder with its own index

A simple project could look like e.g.

.. code-block:: python

    Goethe("myproj")
    FlatChapter("overview")
    DeepChapter("depper_level)
        FlatChapter("overview")
        DeepChapter("second_chapter")


with following file structure:

.. code-block:: python

    ./
    index.rst
    overview.rst

    ./deeper_level
    index.rst
    overview.rst

    ./deeper_level/second_chapter
    index.rst

Features
********

- setup a RST project
- export to dict, files or html
- flat and deep chapters to build unlimited depth of documentation
- modules of RST:
    - toctree
    - paragraph

Backlog
*******

Examples
********

Visualized examples can be found in the ``examples`` folder.

License
*******

Distributed under the MIT License. See ``LICENSE`` for more info.

Backlog
*******

Changelog
*********

Development
===========
