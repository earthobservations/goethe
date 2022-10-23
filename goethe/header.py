from goethe.core import Core


class Header(Core):
    @property
    def header(self):
        return self._header

    @property
    def underline(self):
        return len(self.header) * self._underline

    def __init__(self, header: str, underline: str = "#"):
        super(Header, self).__init__()
        if not underline or len(underline) > 1 or underline == " ":
            raise ValueError("underline has to be one actual character")

        self._header = header.header if type(header) == Header else header
        self._underline = header.underline if type(header) == Header else underline

    def render(self):
        return f"{self.header}\n{self.underline}"
