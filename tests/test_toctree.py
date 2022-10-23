import pytest

from goethe import DeepChapter, FlatChapter, Header, Paragraph, Section, TocTree


def test_toctree_default():
    toctree = TocTree([FlatChapter("flat_chapter"), DeepChapter("deep_chapter")])

    assert toctree.render() == ".. toctree:: \n\n   flat_chapter\n   deep_chapter/index\n"


@pytest.mark.parametrize("content", (Header, Paragraph, Section))
def test_toctree_not_allowed_content(content):
    with pytest.raises(TypeError):
        TocTree([content("abc")])
