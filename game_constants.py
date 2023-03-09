class GameConstants:
    
    # WINDOW
    WIN_CAPTION = 'Minesweeper'
    WIN_WIDTH = 640
    WIN_HEIGHT = 480

    # COLORS
    BLACK = (0, 0, 0)

    # GAME
    BOMB_COUNT = 100
    FIELD_SIZE = 20

    # IMAGES
    DIGIT_X = 0
    DIGIT_Y = 0
    DIGIT_WIDTH = 14
    DIGIT_HEIGHT = 23
    DIGIT_COUNT = 10

    FACES_X = 0
    FACES_Y = 25
    FACES_WIDTH = 27
    FACES_HEIGHT = 26
    FACES_COUNT = 5

    CELL_X = 0
    CELL_Y = 50
    CELL_WIDTH = 17
    CELL_HEIGHT = 17
    CELL_COUNT = 8

    D_CELL_X = 0
    D_CELL_Y = 67
    D_CELL_WIDTH = 17
    D_CELL_HEIGHT = 17
    D_CELL_COUNT = 8

    # SPRITE IMG INDEX
    DIG_0 = 9
    DIG_1 = 0
    DIG_2 = 1
    DIG_3 = 2
    DIG_4 = 3
    DIG_5 = 4
    DIG_6 = 5
    DIG_7 = 6
    DIG_8 = 7
    DIG_9 = 8

    FACE_OK = 0
    FACE_OK_PUSH = 1
    FACE_WOW = 2
    FACE_WIN = 3
    FACE_LOSE = 4

    CELL_OK = 0
    CELL_PUSH = 1
    CELL_EMPTY = 1
    CELL_FLAG = 2
    CELL_UNKNOWN = 3
    CELL_UNKNOWN_PUSH = 4
    CELL_BOMB = 5
    CELL_BOMB_DETONATED = 6
    CELL_BOMB_FOUND = 7
