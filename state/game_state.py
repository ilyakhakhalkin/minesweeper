from game_constants import GameConstants
from .status_face import StatusFace
from .field import Field


class GameState:

    def __init__(self) -> None:
        self.num_bombs = GameConstants.BOMB_COUNT
        self.num_flags_left = GameConstants.BOMB_COUNT
        self.num_flags_placed = 0
        self.found_bombs = 0

        self.field = Field(num_rows=GameConstants.FIELD_SIZE,
                           num_cols=GameConstants.FIELD_SIZE)
        self.started = False
        self.is_game_win = False
        self.is_game_over = False
        self.pushed = []

        self.status_face = StatusFace(308, 5)

    def reveal(self, r, c, skip=False):
        cell = self.field.cells[r][c]

        if not cell.is_accessible_for('reveal'):
            return

        if skip:
            cell.is_pushed = False
            return

        cell.is_revealed = True

        if cell.is_bomb:
            cell.is_detonated = True
            self.game_over()
            return

        if cell.neighboring_mines == 0:
            self.reveal_neighbours(r=r, c=c)

    def reveal_neighbours(self, r, c):
        for row in range(r - 1, r + 2):
            if row < 0 or row >= self.field.num_rows:
                continue

            for col in range(c - 1, c + 2):
                if (
                    (row == r and col == c)
                    or col < 0
                    or col >= self.field.num_cols
                ):
                    continue

                cell = self.field.cells[row][col]

                if cell.is_revealed or cell.is_bomb:
                    continue

                cell.is_revealed = True

                if cell.neighboring_mines == 0:
                    self.reveal_neighbours(r=row, c=col)

    def push(self, r, c):
        cell = self.field.cells[r][c]

        self.clear_push()

        if not cell.is_accessible_for('push'):
            return

        cell.is_pushed = True
        self.pushed.append((r, c))
        self.status_face.status = 'CAUTION'

    def clear_push(self):
        self.status_face.status = 'OK'
        while self.pushed:
            row, col = self.pushed.pop()
            self.field.cells[row][col].is_pushed = False

    def mark(self, r, c):
        cell = self.field.cells[r][c]

        if not cell.is_accessible_for('mark'):
            return

        if cell.is_flagged:
            cell.is_flagged = False
            cell.is_unknown = True
            self.num_flags_placed -= 1
            self.num_flags_left += 1

            if cell.is_bomb:
                self.found_bombs -= 1

        elif cell.is_unknown:
            cell.is_unknown = False

        else:
            if self.num_flags_left < 1:
                return

            cell.is_flagged = True
            self.num_flags_placed += 1
            self.num_flags_left -= 1

            if cell.is_bomb:
                self.found_bombs += 1

            if self.found_bombs == self.num_bombs:
                self.game_win()

    def game_over(self):
        self.is_game_over = True
        self.status_face.status = 'GAME_OVER'
        self.reveal_all()

    def game_win(self):
        self.is_game_won = True
        self.status_face.status = 'WIN'
        self.reveal_all()

    def reveal_all(self):
        for row in self.field.cells:
            for cell in row:
                cell.is_revealed = True
