

class StatusFace:
    def __init__(self, left, top) -> None:
        self.left = left
        self.top = top
        self._status = 0

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        if val == 'OK':
            self._status = 0

        elif val == 'PUSH':
            self._status = 1

        elif val == 'CAUTION':
            self._status = 2

        elif val == 'WIN':
            self._status = 3

        elif val == 'GAME_OVER':
            self._status = 4
