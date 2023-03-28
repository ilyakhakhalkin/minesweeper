# minesweeper
Classic puzzle game. Created with Pygame.


## How to run
0. Create virtual environment:
`python -m venv venv`

1. Activate venv:
`. venv/bin/activate`

2. Install pygame to your venv:
`pip install pygame`

3. Run minesweeper.py:
`python minesweeper.py`

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
- fix bug with reveal_neighbours
- redesign architecture
- optimize init_bombs
- optimize reveal_neighbours
- implement game settings
- implement resizible GUI
- implement timers and counters
- implement multiplayer modes