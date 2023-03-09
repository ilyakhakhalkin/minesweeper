import sys
import random
import pygame
from pygame.math import Vector2

from cells import *
from game_constants import *
from utils.SpriteSheet import SpriteSheet
from utils.SpriteSheet import Stack


pygame.init()

cell_size = Vector2(GameConstants.CELL_WIDTH, GameConstants.CELL_HEIGHT)
screen = pygame.display.set_mode((cell_size.x * GameConstants.FIELD_SIZE,
                                  cell_size.y * GameConstants.FIELD_SIZE))
pygame.display.set_caption(GameConstants.WIN_CAPTION)

clock = pygame.time.Clock()
gamefield = []

sprite_sheet = SpriteSheet('Assets/icons.png')

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

DIGITS = sprite_sheet.load_strip(RECT_DIGITS, GameConstants.DIGIT_COUNT)
DIGITS[0], DIGITS[-1] = DIGITS[-1], DIGITS[0]  # to keep natural order of sprites

FACES = sprite_sheet.load_strip(RECT_FACES, GameConstants.FACES_COUNT)
CELLS = sprite_sheet.load_strip(RECT_CELL, GameConstants.CELL_COUNT)
D_CELLS = sprite_sheet.load_strip(RECT_D_CELL, GameConstants.D_CELL_COUNT)




class GameState:

    def __init__(self) -> None:
        self.field_size = GameConstants.FIELD_SIZE
        self.bomb_count = GameConstants.BOMB_COUNT
        self.flags_count = self.bomb_count
        self.found_bombs = 0

        self.field = self.get_empty_field()
        self.started = False

    def get_empty_field(self):
        return [
            [BasicCell(x=elem, y=row) for elem in range(self.field_size)]
            for row in range(self.field_size)
        ]
    
    def generate_bombs(self, start: Vector2):
        i = 0
        while i < self.bomb_count:
            bomb_pos = Vector2(random.randint(0, self.field_size - 1),
                               random.randint(0, self.field_size - 1))
            
            if not (bomb_pos == start.pos or 
                    isinstance(self.field[bomb_pos.x][bomb_pos.y], BombCell)
                ):
                self.field[bomb_pos.x][bomb_pos.y] = BombCell(bomb_pos)
                i += 1

    def calculate_surroundings(self):

        for row in range(self.field_size):
            bomb_counter = 0

            for elem in range(self.field_size):

                if isinstance(self.field[row][elem], BombCell):
                    continue

                for vert in range(row - 1, row + 2):
                    if vert < 0 or vert >= self.field_size:
                        continue

                    for horiz in range(elem - 1, elem + 2):
                        if horiz < 0 or horiz >= self.field_size:
                            continue
                        if isinstance(self.field[vert][horiz], BombCell):
                            bomb_counter += 1
        
                self.field[row][elem] = InfoCell(Vector2(elem, row),
                                                 value=bomb_counter)
                bomb_counter = 0


class UserInterface:
    def __init__(self) -> None:
        pygame.init()

        self.game_state = GameState()
        self.modified_elements = Stack()
        self.clock = pygame.time.Clock()
        self.running = True

        self.cell_size = Vector2(
            GameConstants.CELL_WIDTH,
            GameConstants.CELL_HEIGHT
        )

        self.window = pygame.display.set_mode(
            self.cell_size.x * self.game_state.field_size,
            self.cell_size.y * self.game_state.field_size
        )
        pygame.display.set_caption(GameConstants.WIN_CAPTION)

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state.__init__()
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                button_down = True
                elem = game.get_cell_by_mouse_position(event.pos)

                if elem.state != GameConstants.CELL_FLAG:
                    elem.state += 1

            elif event.type == pygame.MOUSEMOTION and button_down:
                if elem.state == GameConstants.CELL_PUSH or elem.state == GameConstants.CELL_UNKNOWN:
                    elem.state -= 1

                elem = game.get_cell_by_mouse_position(event.pos)
                if elem.state == GameConstants.CELL_OK or elem.state == GameConstants.CELL_UNKNOWN:
                    elem.state += 1

            elif event.type == pygame.MOUSEBUTTONUP:
                button_down = False
                elem = game.get_cell_by_mouse_position(event.pos)

                if elem.state != GameConstants.CELL_FLAG:
                    elem.state -= 1

                if event.button == pygame.BUTTON_RIGHT:
                    if elem.state == GameConstants.CELL_FLAG:
                        game._flags_count -= 1
                        if isinstance(game.field[elem.y][elem.x], BombCell):
                            game.found_bombs -= 1

                    elem.next_state()

                    if elem.state == GameConstants.CELL_FLAG:
                        game._flags_count += 1
                        if isinstance(game.field[elem.y][elem.x], BombCell):
                            game.found_bombs += 1

                elif event.button == pygame.BUTTON_LEFT and elem.state == GameConstants.CELL_OK:

                    if isinstance(elem, BasicCell) and not game.started:
                        game.generate_bombs(start=elem.pos)
                        game.calculate_surroundings()
                        game.started = True
                        elem = game.field[elem.y][elem.x]
                    elem.active = True

                    if isinstance(elem, BombCell):
                        elem.state = GameConstants.CELL_PUSH
                        game.detonate()                    

                    elif elem.value == 0:
                        game.activate_nearby_cells(elem)

    def get_cell_by_position(self, pos: Vector2):
 
        pos.x //= GameConstants.CELL_WIDTH
        pos.y //= GameConstants.CELL_HEIGHT
        
        if pos >= Vector2(0, 0) and pos <= Vector2(self.game_state.field_size,
                                                   self.game_state.field_size):
            return self.field[pos.y][pos.x]

        return BasicCell()

    def update(self):
        pass
    
    def render(self):
        if self.game_state.started == False:
            screen.fill(GameConstants.BLACK)

        pygame.display.update()

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()


class Game:
    
    def __init__(self, field_size, bomb_count) -> None:
        self._field_size = field_size
        self._bomb_count = bomb_count
        self._flags_count = bomb_count
        self.field = self.get_empty_field()
        self.started = False
        self._found_bombs = 0

    def restart(self):
        self._flags_count = self._bomb_count
        self.field = self.get_empty_field()
        self.started = False
        self._found_bombs = 0

    @property
    def found_bombs(self):
        return self._found_bombs

    @found_bombs.setter
    def found_bombs(self, val):
        self._found_bombs = val
        print(self._found_bombs, self._bomb_count)
        if self._found_bombs == self._bomb_count:
            print('Win!!!')
    
    def get_empty_field(self):
        field = []

        for row_idx in range(self._field_size):
            row = []
            
            for elem_idx in range(self._field_size):
                row.append(BasicCell(x=elem_idx, y=row_idx))

            field.append(row)

        return field

    def generate_bombs(self, restricted_elem):
        i = 0
        while i < self._bomb_count:

            bomb_x = random.randint(0, self._field_size - 1)
            bomb_y = random.randint(0, self._field_size - 1)
            
            if bomb_x == restricted_elem.x and bomb_y == restricted_elem.y:
                # i -= 1
                continue

            if isinstance(self.field[bomb_y][bomb_x], BombCell):
                # i -= 1
                continue

            self.field[bomb_y][bomb_x] = BombCell(x=bomb_x, y=bomb_y)
            i += 1

    def calculate_surroundings(self):

        for row_idx in range(self._field_size):
            bomb_counter = 0
            
            for elem_idx in range(self._field_size):
                
                if isinstance(self.field[row_idx][elem_idx], BombCell):
                    continue

                for vert in range(row_idx - 1, row_idx + 2):
                    if vert < 0 or vert >= self._field_size:
                        continue
                    
                    for horiz in range(elem_idx - 1, elem_idx + 2):
                        if horiz < 0 or horiz >= self._field_size:
                            continue
                        if isinstance(self.field[vert][horiz], BombCell):
                            bomb_counter += 1
        
                self.field[row_idx][elem_idx] = InfoCell(x=elem_idx,
                                                            y=row_idx,
                                                            value=bomb_counter)
                bomb_counter = 0

    def get_cell_by_mouse_position(self, pos):

        x = int(pos[0] / GameConstants.CELL_WIDTH)
        y = int(pos[1] / GameConstants.CELL_HEIGHT)

        if (
            self._field_size > x >= 0 and
            self._field_size > y >= 0
        ):
            return self.field[y][x]

        return BasicCell()

    def activate_nearby_cells(self, safe_cell):
        for row_idx in range(safe_cell.y - 1, safe_cell.y + 2):
            if row_idx < 0:
                continue
            if row_idx >= GameConstants.FIELD_SIZE:
                break
            
            for elem_idx in range(safe_cell.x - 1, safe_cell.x + 2):
                if elem_idx < 0:
                    continue
                if elem_idx >= GameConstants.FIELD_SIZE:
                    break
                
                elem = self.field[row_idx][elem_idx]

                if elem.active or elem == safe_cell or isinstance(elem, BombCell):
                    continue
                
                elem.active = True

                if elem.value == 0:
                    self.activate_nearby_cells(elem)

    def detonate(self):
        for line in self.field:
            for elem in line:
                elem.active = True


if __name__ == '__main__':

    screen.fill(GameConstants.BLACK)
    
    game = Game(
        field_size=GameConstants.FIELD_SIZE,
        bomb_count=GameConstants.BOMB_COUNT
    )

    done = False
    
    button_down = False
    elem = BasicCell()
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.restart()
                    pygame.display.update()
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                button_down = True
                elem = game.get_cell_by_mouse_position(event.pos)

                if elem.state != GameConstants.CELL_FLAG:
                    elem.state += 1

            elif event.type == pygame.MOUSEMOTION and button_down:
                if elem.state == GameConstants.CELL_PUSH or elem.state == GameConstants.CELL_UNKNOWN:
                    elem.state -= 1

                elem = game.get_cell_by_mouse_position(event.pos)
                if elem.state == GameConstants.CELL_OK or elem.state == GameConstants.CELL_UNKNOWN:
                    elem.state += 1
            
            elif event.type == pygame.MOUSEBUTTONUP:
                button_down = False
                elem = game.get_cell_by_mouse_position(event.pos)
                if elem.state != GameConstants.CELL_FLAG:
                    elem.state -= 1

                if event.button == pygame.BUTTON_RIGHT and game.started:
                    if elem.state == GameConstants.CELL_FLAG:
                        game._flags_count -= 1
                        if isinstance(game.field[elem.y][elem.x], BombCell):
                            game.found_bombs -= 1

                    elem.next_state()

                    if elem.state == GameConstants.CELL_FLAG:
                        game._flags_count += 1
                        if isinstance(game.field[elem.y][elem.x], BombCell):
                            game.found_bombs += 1

                elif event.button == pygame.BUTTON_LEFT and elem.state == GameConstants.CELL_OK:
    
                    if isinstance(elem, BasicCell) and not game.started:
                        game.generate_bombs(restricted_elem=elem)
                        game.calculate_surroundings()
                        game.started = True
                        elem = game.field[elem.y][elem.x]

                    elem.active = True
                    if isinstance(elem, BombCell):
                        elem.state = GameConstants.CELL_PUSH
                        game.detonate()                    

                    elif elem.value == 0:
                        game.activate_nearby_cells(elem)

        pygame.display.update()
        clock.tick(10000)

# pygame.quit()
