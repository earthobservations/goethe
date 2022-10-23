from goethe.paragraph import Paragraph


def test_paragraph_default():
    paragraph = Paragraph(paragraph="Just a normal paragraph.")
    assert paragraph.render() == "Just a normal paragraph."


def test_paragraph_indent():
    paragraph = Paragraph(paragraph="Just a normal paragraph.", indent=4)
    assert paragraph.render() == "    Just a normal paragraph."
