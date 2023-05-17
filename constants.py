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

NOT_RIGHT_EDGE = int("0b0111111101111111011111110111111101111111011111110111111101111111", 2)
NOT_LEFT_EDGE = int("0b1111111011111110111111101111111011111110111111101111111011111110", 2)
NOT_EDGES = NOT_RIGHT_EDGE & (NOT_RIGHT_EDGE << 1)
MAX_VALUE = int("0b1111111111111111111111111111111111111111111111111111111111111111", 2)  # for bitwise inversion


# Bitboards for each square
A1 = 2 ** 0
B1 = 2 ** 1
C1 = 2 ** 2
D1 = 2 ** 3
E1 = 2 ** 4
F1 = 2 ** 5
G1 = 2 ** 6
H1 = 2 ** 7
A2 = 2 ** 8
B2 = 2 ** 9
C2 = 2 ** 10
D2 = 2 ** 11
E2 = 2 ** 12
F2 = 2 ** 13
G2 = 2 ** 14
H2 = 2 ** 15
A3 = 2 ** 16
B3 = 2 ** 17
C3 = 2 ** 18
D3 = 2 ** 19
E3 = 2 ** 20
F3 = 2 ** 21
G3 = 2 ** 22
H3 = 2 ** 23
A4 = 2 ** 24
B4 = 2 ** 25
C4 = 2 ** 26
D4 = 2 ** 27
E4 = 2 ** 28
F4 = 2 ** 29
G4 = 2 ** 30
H4 = 2 ** 31
A5 = 2 ** 32
B5 = 2 ** 33
C5 = 2 ** 34
D5 = 2 ** 35
E5 = 2 ** 36
F5 = 2 ** 37
G5 = 2 ** 38
H5 = 2 ** 39
A6 = 2 ** 40
B6 = 2 ** 41
C6 = 2 ** 42
D6 = 2 ** 43
E6 = 2 ** 44
F6 = 2 ** 45
G6 = 2 ** 46
H6 = 2 ** 47
A7 = 2 ** 48
B7 = 2 ** 49
C7 = 2 ** 50
D7 = 2 ** 51
E7 = 2 ** 52
F7 = 2 ** 53
G7 = 2 ** 54
H7 = 2 ** 55
A8 = 2 ** 56
B8 = 2 ** 57
C8 = 2 ** 58
D8 = 2 ** 59
E8 = 2 ** 60
F8 = 2 ** 61
G8 = 2 ** 62
H8 = 2 ** 63
