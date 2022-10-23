import pytest

from goethe.header import Header


def test_header_default():
    header = Header("NormalHeader")
    assert header.render() == "NormalHeader\n############"


def test_header_underline():
    header = Header("NormalHeader", "*")
    assert header.render() == "NormalHeader\n************"


def test_header_false_underline():
    with pytest.raises(ValueError):
        Header("NormalHeader", "*#")
