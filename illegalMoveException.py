
class IllegalMoveException(Exception):
    """Exception raised for illegal move in the game."""

    def __init__(self, move, message="Move is not legal."):
        self.move = move
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.move} -> {self.message}'