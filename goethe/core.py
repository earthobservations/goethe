import uuid


class Core:
    @property
    def cid(self):
        return self._cid

    def __init__(self):
        self._cid = uuid.uuid4()
