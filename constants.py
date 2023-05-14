BOARD_SIZE = 8
WHITE = 0
BLACK = 1
PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6
KING = 7
LABELS = {
    WHITE: "White",
    BLACK: "Black",
    PAWN: "Pawns",
    KNIGHT: "Knights",
    BISHOP: "Bishops",
    ROOK: "Rooks",
    QUEEN: "Queens",
    KING: "Kings",
}

RIGHT_EDGE = int("0b0111111101111111011111110111111101111111011111110111111101111111", 2)
LEFT_EDGE = int("0b1111111011111110111111101111111011111110111111101111111011111110", 2)
BOTH_EDGES = RIGHT_EDGE & (RIGHT_EDGE << 1)
MAX_VALUE = int("0b1111111111111111111111111111111111111111111111111111111111111111", 2) # for bitwise inversion