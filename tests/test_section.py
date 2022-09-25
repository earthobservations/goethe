from collections import OrderedDict

import pytest
from pytest_lazyfixture import lazy_fixture

from goethe import DeepChapter, FlatChapter, Header, Paragraph, Section


@pytest.fixture
def paragraph_normal():
    return Paragraph("NormalText")


@pytest.fixture
def paragraph_indent():
    return Paragraph("NormalText", indent=4)


@pytest.fixture
def header_normal():
    return Header("NormalHeader")


@pytest.fixture
def header_custom():
    return Header("NormalHeader", "*")


@pytest.fixture(
    params=[["NormalText", lazy_fixture("paragraph_normal")], [lazy_fixture("paragraph_normal"), "NormalText"]]
)
def content_list(request):
    return request.param


@pytest.mark.parametrize("header", ["NormalHeader", lazy_fixture("header_normal")])
def test_section_empty(header):
    assert Section(header).render() == "NormalHeader\n############\n\n"


def test_section_empty_header_custom(header_custom):
    assert Section(header_custom).render() == "NormalHeader\n************\n\n"


@pytest.mark.parametrize("header", ["NormalHeader", lazy_fixture("header_normal")])
@pytest.mark.parametrize("content", ["NormalText", lazy_fixture("paragraph_normal")])
def test_section_content_normal(header, content):
    assert Section(header, content=content).render() == "NormalHeader\n############\n\nNormalText"

    section = Section(header)
    section.add_content(content)
    assert section.render() == "NormalHeader\n############\n\nNormalText"


@pytest.mark.parametrize("header", ["NormalHeader", lazy_fixture("header_normal")])
def test_section_content_paragraph_indent(header, paragraph_indent):
    assert Section(header, content=paragraph_indent).render() == "NormalHeader\n############\n\n    NormalText"

    section = Section(header)
    section.add_content(paragraph_indent)
    assert section.render() == "NormalHeader\n############\n\n    NormalText"


@pytest.mark.parametrize("header", ["NormalHeader", lazy_fixture("header_normal")])
@pytest.mark.parametrize(
    "content_list",
    [
        ["NormalText", Paragraph("NormalText")],
        [
            Paragraph("NormalText"),
            "NormalText",
        ],
    ],
)
def test_section_content_list(header, content_list):
    assert Section(header, content=content_list).render() == "NormalHeader\n############\n\nNormalText\n\nNormalText"

    section = Section(header)
    section.add_content(content_list)
    assert section.render() == "NormalHeader\n############\n\nNormalText\n\nNormalText"


@pytest.mark.parametrize("name", ["NormalName", Header("NormalName")])
@pytest.mark.parametrize("header", ["NormalHeader", Header("NormalHeader")])
def test_section_different_name_and_header(name, header):
    assert Section(name=name, header=header).render() == "NormalHeader\n############\n\n"


@pytest.mark.parametrize("header", ["NormalHeader", lazy_fixture("header_normal")])
@pytest.mark.parametrize("content", ["NormalText", lazy_fixture("paragraph_normal")])
def test_section_content_normal_to_dict(header, content):
    assert Section(name=header, content=content).to_dict() == OrderedDict(
        {"name": "NormalHeader", "header": "NormalHeader", "text": "NormalHeader\n############\n\nNormalText"}
    )


@pytest.mark.parametrize("name", ["NormalName", Header("NormalName")])
@pytest.mark.parametrize("header", ["NormalHeader", Header("NormalHeader")])
def test_section_name_header_to_dict(name, header):
    assert Section(name=name, header=header).to_dict() == OrderedDict(
        {"name": "NormalName", "header": "NormalHeader", "text": "NormalHeader\n############\n\n"}
    )


@pytest.mark.parametrize("content", (Header, FlatChapter, DeepChapter))
def test_section_not_allowed_content(content):
    with pytest.raises(TypeError):
        Section("NormalHeader", content=[content()])
