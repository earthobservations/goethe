import logging
from copy import copy
from typing import TYPE_CHECKING, List, Optional, Union

from numpy.distutils.misc_util import as_list

from goethe.core import Core

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from goethe.header import Header
    from goethe.paragraph import Paragraph
    from goethe.section import Section

_CONTENT_TYPE = Union[str, "Header", "Paragraph", "Section"]


class _Content(Core):
    _ctypes = None

    def __init__(self, content: Optional[Union[_CONTENT_TYPE, List[_CONTENT_TYPE]]] = None):
        super(_Content, self).__init__()

        # TODO: change this
        try:
            content = content._content
        except AttributeError:
            pass

        content = as_list(content or [])

        self._assert_ctypes(content)

        self._content = content

    def __iter__(self):
        for c in self._content:
            yield c

    @classmethod
    def copy(cls):
        return copy(cls)

    def _assert_ctypes(self, content: Union[List[_CONTENT_TYPE], _CONTENT_TYPE]):
        from goethe.chapter import DeepChapter, FlatChapter
        from goethe.header import Header
        from goethe.paragraph import Paragraph
        from goethe.section import Section

        ctypes = self._ctypes or [str, Paragraph, Header, Section, FlatChapter, DeepChapter]
        ctypes = [*ctypes, _Content]

        for c in as_list(content):
            if type(c) not in ctypes and not issubclass(type(c), _Content):
                raise TypeError(f"content {type(c)} does not match any of {[c.__name__ for c in ctypes]}")

    def find_content(self, cid: str):
        for c in self._content:
            if c.cid == cid:
                return c
        log.info(f"content with id {cid} not found")
        return None

    def add_content(self, content: _CONTENT_TYPE):
        content = content or []
        content = as_list(content)
        self._assert_ctypes(content)
        self._content.extend(content)

    def remove_content(self, cid: str):
        content = self.find_content(cid)
        self._content.remove(content)

    def clear(self):
        self._content.clear()

    def render(self) -> str:
        return "\n\n".join([c.render() for c in self._content])


class ContentFactory:
    def __new__(cls, ctypes=None):
        from goethe.chapter import DeepChapter, FlatChapter
        from goethe.header import Header
        from goethe.paragraph import Paragraph
        from goethe.section import Section

        ctypes = ctypes or [str, Paragraph, Header, Section, FlatChapter, DeepChapter]
        ctypes = [*ctypes, _Content]

        class Content(_Content):
            _ctypes = ctypes

        return Content
