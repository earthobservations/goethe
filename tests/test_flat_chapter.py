import pytest

from goethe import DeepChapter, FlatChapter, Header


@pytest.fixture
def flat_chapter():
    return FlatChapter("abc", "abc")


def test_flat_chapter_default(flat_chapter):
    assert flat_chapter.render() == "abc\n###\n\nabc"


@pytest.mark.parametrize("content", (Header, DeepChapter))
def test_flat_chapter_not_allowed_content(content):
    with pytest.raises(TypeError):
        FlatChapter("NormalHeader", content=[content()])


def test_flat_chapter_write(tmp_path, flat_chapter):
    tmp_file = tmp_path / "flat_chapter.rst"
    tmp_file.unlink(missing_ok=True)
    flat_chapter.to_rst(tmp_file)
    assert tmp_file.open().read() == "abc\n###\n\nabc"
