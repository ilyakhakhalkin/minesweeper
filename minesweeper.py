import pygame

from utils.SpriteSheet import SpriteSheet
from state.game_state import GameState
from game_constants import GameConstants

pygame.init()


class GUI:
    """
    Stores graphic Surface objects.
    """
    def __init__(self) -> None:
        sprite_sheet = SpriteSheet('Assets/icons_big.png')

        RECT_CELL = (
            GameConstants.CELL_X,
            GameConstants.CELL_Y,
            GameConstants.CELL_WIDTH,
            GameConstants.CELL_HEIGHT
        )
        RECT_DIGITS = (
            GameConstants.DIGIT_X,
            GameConstants.DIGIT_Y,
            GameConstants.DIGIT_WIDTH,
            GameConstants.DIGIT_HEIGHT
        )
        RECT_D_CELL = (
            GameConstants.D_CELL_X,
            GameConstants.D_CELL_Y,
            GameConstants.D_CELL_WIDTH,
            GameConstants.D_CELL_HEIGHT
        )
        RECT_FACES = (
            GameConstants.FACES_X,
            GameConstants.FACES_Y,
            GameConstants.FACES_WIDTH,
            GameConstants.FACES_HEIGHT
        )

        self.DIGITS = sprite_sheet.load_strip(
            RECT_DIGITS,
            GameConstants.DIGIT_COUNT
        )
        self.FACES = sprite_sheet.load_strip(
            RECT_FACES,
            GameConstants.FACES_COUNT
        )
        self.CELLS = sprite_sheet.load_strip(
            RECT_CELL,
            GameConstants.CELL_COUNT
        )
        self.D_CELLS = sprite_sheet.load_strip(
            RECT_D_CELL,
            GameConstants.D_CELL_COUNT
        )


class UserInterface:
    """
    Main class.
    """
    def __init__(self) -> None:
        pygame.init()

        self.game_state = GameState()
        self.running = True
        self.button_down = False
        self.skip_click = False

        win_width = int(
            GameConstants.CELL_WIDTH * self.game_state.field.num_rows
        )
        win_height = (
            int(GameConstants.CELL_HEIGHT * self.game_state.field.num_cols)
            +
            GameConstants.STATUS_BAR_HEIGHT
        )
        self.window = pygame.display.set_mode((win_width, win_height))
        self.GUI = GUI()
        pygame.display.set_caption(GameConstants.WIN_CAPTION)

    def process_input(self):
        """
        Handling events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state.__init__()
                    break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_down = True
                if self.is_status_face_clicked(event.pos):
                    self.game_state.status_face.status = 'PUSH'

                r, c = self.parse_mouse_position(event.pos)

                if not (r is None) and not (c is None):
                    self.game_state.push(r=r, c=c)

            elif event.type == pygame.MOUSEMOTION and self.button_down:
                self.skip_click = True
                r, c = self.parse_mouse_position(event.pos)
                if not (r is None) and not (c is None):
                    self.game_state.push(r=r, c=c)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_down = False
                if self.is_status_face_clicked(event.pos):
                    self.game_state.__init__()
                    return

                self.game_state.clear_push()

                r, c = self.parse_mouse_position(event.pos)
                if r is None or c is None:
                    return

                if not self.game_state.started:
                    self.game_state.started = True
                    self.game_state.field.init_bombs(
                        num_bombs=self.game_state.num_bombs,
                        avoid_r=r,
                        avoid_c=c
                    )
                    self.game_state.field.init_cells()

                if self.skip_click:
                    self.game_state.reveal(r=r, c=c, skip=True)
                    self.skip_click = False

                if event.button == pygame.BUTTON_RIGHT:
                    self.game_state.mark(r=r, c=c)

                if event.button == pygame.BUTTON_LEFT:
                    self.game_state.reveal(r=r, c=c)

    def parse_mouse_position(self, pos):
        """
        Identify row and column of cell by mouse position.
        pos[0] - x
        pos[1] - y
        """

        r = pos[0] // GameConstants.CELL_WIDTH
        c = (
            (pos[1] - GameConstants.STATUS_BAR_HEIGHT)
            // GameConstants.CELL_HEIGHT
        )

        if (
            0 <= r < self.game_state.field.num_rows and
            0 <= c < self.game_state.field.num_cols
        ):
            return (r, c)

        return (None, None)

    def is_status_face_clicked(self, pos):
        return (
            pos[0] > self.game_state.status_face.left and
            pos[0] < (self.game_state.status_face.left
                      + GameConstants.FACES_WIDTH)
            and
            pos[1] > self.game_state.status_face.top and
            pos[1] < (self.game_state.status_face.top
                      + GameConstants.FACES_HEIGHT)
        )

    def render(self):
        """
        Render all cells.
        """
        self.window.blit(
                self.GUI.FACES[self.game_state.status_face.status],
                (
                    self.game_state.status_face.left,
                    self.game_state.status_face.top
                )
            )

        for row in self.game_state.field.cells:
            for cell in row:

                if cell.is_revealed:

                    if cell.is_bomb:
                        if cell.is_detonated:
                            image = self.GUI.CELLS[
                                GameConstants.CELL_BOMB_DETONATED
                            ]

                        elif cell.is_flagged:
                            image = self.GUI.CELLS[
                                GameConstants.CELL_BOMB_FOUND
                            ]

                        else:
                            image = self.GUI.CELLS[GameConstants.CELL_BOMB]

                    elif cell.is_flagged:
                        image = self.GUI.CELLS[GameConstants.CELL_FLAG]

                    elif cell.is_unknown:
                        image = self.GUI.CELLS[GameConstants.CELL_UNKNOWN]

                    elif cell.neighboring_mines == 0:
                        image = self.GUI.CELLS[GameConstants.CELL_PUSH]

                    else:
                        image = self.GUI.D_CELLS[cell.neighboring_mines - 1]

                elif cell.is_pushed:
                    if cell.is_unknown:
                        image = self.GUI.CELLS[GameConstants.CELL_UNKNOWN_PUSH]
                    else:
                        image = self.GUI.CELLS[GameConstants.CELL_PUSH]

                else:
                    if cell.is_unknown:
                        image = self.GUI.CELLS[GameConstants.CELL_UNKNOWN]

                    elif cell.is_flagged:
                        image = self.GUI.CELLS[GameConstants.CELL_FLAG]

                    else:
                        image = self.GUI.CELLS[GameConstants.CELL_OK]

                self.window.blit(
                    image,
                    (
                        cell.row * GameConstants.CELL_WIDTH,
                        (
                            cell.col * GameConstants.CELL_HEIGHT
                            + GameConstants.STATUS_BAR_HEIGHT
                        )
                    ),
                )

        pygame.display.update()

    def run(self):
        while self.running:
            self.process_input()
            self.render()
            pygame.time.delay(20)

        pygame.quit()


if __name__ == '__main__':
    ui = UserInterface()
    ui.run()
