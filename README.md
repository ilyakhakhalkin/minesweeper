# minesweeper
Classic puzzle game. Created with Pygame.


## How to run
0. Install Python if you don't have it yet:
`https://www.python.org/downloads/`

1. Clone repository:
`git clone git@github.com:ilyakhakhalkin/minesweeper.git`

2. Create virtual environment:
`python -m venv venv`
or
`python3 -m venv venv`

3. Activate venv:

- macos:
`. venv/bin/activate`

- win:
`source venv/Scripts/activate`

- see also:
`https://docs.python.org/3/library/venv.html`

4. Install pygame to your venv:
`pip install pygame`
or
`pip3 unstall pygame`

5. Run minesweeper.py:
`python minesweeper.py`
or
`python3 minesweeper.py`

## Description
#### class Cell:
Stores state of cell:
- row number
- col number
- is it a bomb
- is it revealed
- is it flagged
- is it unknown
- count of neighboring mines
- is it pushed
- is it detonated

Methods:
- is_accessible_for(action: str): returns True if action is allowed


#### class Field:
Stores game field - 2D array of cells.

Methods:
- init_empty: Populates array with non-bomb cells only
- init_bombs: Turns random cells into bombs
- init_cells: Calculates neighbouring mines count for non-bomb cells


#### class GameState:
Game state and cell logic here.

Methods:
- reveal: Change cell state to revealed (if allowed)
- reveal_neighbours: Reveal neighbouring cells if empty cell was revealed
- push: Change cell state to pushed (if allowed)
- clear_push: Unpush previous cells
- mark: Mark or unmark cell with flag/question
- game_over and game_win: Change game state and trigger revealing of all cells
- reveal_all: Change state of all cells to revealed


#### class GameConstants:
Stores game settings


#### class UserIntereface:
Main class.

Methods:
- run: main loop
- process_input: event loop processing
- render: draw current state


### Backlog
Todo:
- fix some bugs
- redesign architecture
- optimize init_bombs
- optimize reveal_neighbours
- implement game settings
- implement resizible GUI
- implement timers and counters
- implement multiplayer modes
