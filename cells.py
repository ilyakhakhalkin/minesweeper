import pygame

from game_constants import *
from minesweeper import screen
from minesweeper import CELLS, D_CELLS

class BasicCell:
    def __init__(self, x: int=-50, y: int=-50) -> None:
        self.x = x
        self.y = y
        self._active = False
        self.state = GameConstants.CELL_OK

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val):
        self._active = val
        self.update_image()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val
        self.update_image()

    def next_state(self):
        if self.state >= GameConstants.CELL_UNKNOWN:
            self.state = GameConstants.CELL_OK
        else:
            self.state += 1
            if self.state == 1:
                self.state = 2

    def update_image(self):
        image = CELLS[self.state]
        self.print_image(image)

    def print_image(self, image):
        screen.blit(
            image,
            (self.x * GameConstants.CELL_WIDTH, self.y * GameConstants.CELL_HEIGHT),
        )


class InfoCell(BasicCell):
    def __init__(self, x: int, y: int, value: int) -> None:
        self.value = value
        self._active = False
        super().__init__(x, y)

    def update_image(self):
        if not self.active:
            super().update_image()
            return

        if self.value == 0:
            image = CELLS[GameConstants.CELL_EMPTY]
        else:
            image = D_CELLS[self.value - 1]

        self.print_image(image)


class BombCell(BasicCell):
    def __init__(self, x, y) -> None:
        self._active = False
        super().__init__(x, y)

    def update_image(self):
        if not self.active:
            super().update_image()
            return

        if self.state < GameConstants.CELL_UNKNOWN:
            image = CELLS[self.state + GameConstants.CELL_BOMB]
        else:
            image = CELLS[GameConstants.CELL_BOMB]
        
        self.print_image(image)
