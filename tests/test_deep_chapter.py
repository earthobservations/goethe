import pytest

from goethe import DeepChapter, FlatChapter, Header, Paragraph, TocTree


@pytest.fixture
def flat_chapter():
    return FlatChapter("flat_chapter", "abc")


@pytest.fixture
def deep_chapter(flat_chapter):
    return DeepChapter("deep_chapter", content=[flat_chapter, DeepChapter("deeper_chapter")])


def test_deep_chapter_default(deep_chapter):
    assert (
        deep_chapter.render()
        == "deep_chapter\n############\n\n.. toctree:: \n\n   flat_chapter\n   deeper_chapter/index\n"
    )


@pytest.mark.parametrize("content", (Header, Paragraph, TocTree))
def test_deep_chapter_not_allowed_content(content):
    with pytest.raises(TypeError):
        DeepChapter("NormalHeader", content=[content()])


def test_deep_chapter_write(tmp_path, deep_chapter):
    index_file = tmp_path / "deep_chapter" / "index.rst"
    index_file.unlink(missing_ok=True)
    deep_chapter.to_rst(index_file)
    assert (
        index_file.open().read()
        == "deep_chapter\n############\n\n.. toctree:: \n\n   flat_chapter\n   deeper_chapter/index\n"
    )
    flat_chapter = tmp_path / "deep_chapter" / "flat_chapter.rst"
    assert flat_chapter.open().read() == "flat_chapter\n############\n\nabc"
    deeper_chapter = tmp_path / "deep_chapter" / "deeper_chapter" / "index.rst"
    assert deeper_chapter.open().read() == "deeper_chapter\n##############\n\n.. toctree:: \n\n"
