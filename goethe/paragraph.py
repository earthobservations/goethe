from goethe.core import Core


class Paragraph(Core):
    @property
    def paragraph(self):
        return self._paragraph

    @property
    def indent(self):
        return self._indent * " "

    def __init__(self, paragraph: str, indent: int = 0):
        super(Paragraph, self).__init__()
        self._paragraph = paragraph
        self._indent = int(indent)

    def render(self):
        return "\n".join([f"{self.indent}{line}" for line in self.paragraph.split("\n")])
