class Cell:
    """
    Stores state of cell.
    """
    def __init__(self, r: int, c: int) -> None:
        self.row = r
        self.col = c
        self.is_bomb = False
        self.is_revealed = False
        self.is_flagged = False
        self.is_unknown = False
        self.neighboring_mines = 0
        self.is_pushed = False
        self.is_detonated = False

    def is_accessible_for(self, action: str) -> bool:
        """
        Returns True if action is allowed.
        """
        if action == 'mark':
            return not self.is_revealed

        if self.is_revealed:
            return False

        if action == 'reveal':
            return not (self.is_flagged or self.is_unknown)

        if action == 'push':
            return not self.is_flagged
