import random

from .cells import Cell


class Field:

    def __init__(self, num_rows: int, num_cols: int) -> None:
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.init_empty()

    def init_empty(self):
        self.cells = [
            [
                Cell(r=r, c=c) for c in range(self.num_cols)
            ]
            for r in range(self.num_rows)
        ]

    def init_bombs(self, num_bombs, avoid_r, avoid_c):
        placed = 0

        while placed < num_bombs:
            bomb_r = random.randint(0, self.num_rows - 1)
            bomb_c = random.randint(0, self.num_cols - 1)

            if bomb_r != avoid_r and bomb_c != avoid_c:
                if not self.cells[bomb_r][bomb_c].is_bomb:
                    self.cells[bomb_r][bomb_c].is_bomb = True
                    placed += 1

    def init_cells(self):
        for r in range(self.num_rows):
            bomb_counter = 0

            for c in range(self.num_cols):
                if self.cells[r][c].is_bomb:
                    continue

                for y in range(r - 1, r + 2):
                    if y < 0 or y >= self.num_rows:
                        continue

                    for x in range(c - 1, c + 2):
                        if x < 0 or x >= self.num_cols:
                            continue

                        if self.cells[y][x].is_bomb:
                            bomb_counter += 1

                self.cells[r][c].neighboring_mines = bomb_counter
                bomb_counter = 0
