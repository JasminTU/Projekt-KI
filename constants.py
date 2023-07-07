from loguru import logger

BOARD_SIZE = 8
DRAW = -1
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
NOT_TOP_EDGE = int("0b1111111100000000000000000000000000000000000000000000000000000000", 2) ^ MAX_VALUE
NOT_BOTTOM_EDGE = int("0b0000000000000000000000000000000000000000000000000000000011111111", 2) ^ MAX_VALUE
INITIAL_WHITE_PAWN_POSITIONS = int("0b0000000000000000000000000000000000000000000000001111111100000000", 2)
INITIAL_BLACK_PAWN_POSITIONS = int("0b0000000011111111000000000000000000000000000000000000000000000000", 2)


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

# Piece values and piece square tables: 
# https://www.chessprogramming.org/Simplified_Evaluation_Function
# https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function
# Idea: Take the PST from chess and a a term for center control in the evaluation method()

PIECE_VALUES_MIDGAME = {
    PAWN: 82, KNIGHT: 337, BISHOP: 365, ROOK: 477, QUEEN: 1025, KING: 20000
}
PIECE_VALUES_ENDGAME = {
    PAWN: 94, KNIGHT: 281, BISHOP: 297, ROOK: 512, QUEEN: 936, KING: 20000
}

PAWN_VALUES_OPENING = [
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  6,  12,  17,   6, 10, -25,
    -26,  -4,  3, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0,
]

PAWN_VALUES_MIDGAME = [
      0,   0,   0,   0,   0,   0,  0,   0,
     98, 134,  61,  95,  68, 126, 34, -11,
     -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  6,  12,  17,   6, 10, -25,
    -26,  -4,  3, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
      0,   0,   0,   0,   0,   0,  0,   0,
]

PAWN_VALUES_ENDGAME = [
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0,
]

KNIGHT_VALUES_OPENING = [
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -50, -58, -33, -17, -28, -50,  -23,
]

KNIGHT_VALUES_MIDGAME = [
    -167, -89, -34, -49,  61, -97, -15, -107,
     -73, -41,  72,  36,  23,  62,   7,  -17,
     -47,  60,  37,  65,  84, 129,  73,   44,
      -9,  17,  19,  53,  37,  69,  18,   22,
     -13,   4,  16,  13,  28,  19,  21,   -8,
     -23,  -9,  12,  10,  19,  17,  25,  -16,
     -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23,
]

KNIGHT_VALUES_ENDGAME = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64,
]

BISHOP_VALUES_OPENING = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -40, -21, -13, -40, -39, -21,
]

BISHOP_VALUES_MIDGAME = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
     -4,   5,  19,  50,  37,  37,   7,  -2,
     -6,  13,  13,  26,  34,  12,  10,   4,
      0,  15,  15,  15,  14,  27,  18,  10,
      4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21,
]

BISHOP_VALUES_ENDGAME = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17,
]

ROOK_VALUES_OPENING = [
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -50, -13,   1,  17, 16,  7, -37, -50,
]

ROOK_VALUES_MIDGAME = [
     32,  42,  32,  51, 63,  9,  31,  43,
     27,  32,  58,  62, 80, 67,  26,  44,
     -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26,
]

ROOK_VALUES_ENDGAME = [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20,
]

QUEEN_VALUES_OPENING = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
]

QUEEN_VALUES_MIDGAME = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
]

QUEEN_VALUES_MIDGAME = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
     -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
     -1, -18,  -9,  10, -15, -25, -31, -50,
]

QUEEN_VALUES_ENDGAME = [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41,
]

KING_VALUES_OPENING = [
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, 100000, 100000, -25, -14, -36,
    -49,  -1, -27, 100000, 100000, -44, -33, -51,
    -14, -14, -22, 0,  0, -30, -15, -27,
      1,   7,  -8, 0, 0, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
]

KING_VALUES_MIDGAME = [
    -65,  23,  16, -15, -56, -34,   2,  13,
     29,  -1, -20,  -7,  -8,  -4, -38, -29,
     -9,  24,   100,  100,  100,  100,  22, -22,
    -17, -20, 100, 100000, 100000, 100, -14, -36,
    -49,  -1, 100, 100000, 100000, 100, -33, -51,
    -14, -14, 100,  100,  100,  100, -15, -27,
      1,   7,  -8, 0, 0, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14,
]

KING_VALUES_ENDGAME = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  100,  100,  100,  100,  44,  13,
     -8,  22,  100,  100000,  100000,  100,  26,   3,
    -18,  -4,  100,  100000,  100000,  100,   9, -11,
    -19,  -3,  100,  100,  100,  100,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
]

def get_figure_value(player, position, figure, game_phase):
    if game_phase == "opening":
        if player == WHITE:
            if figure == PAWN:
                return PAWN_VALUES_OPENING[63 - position]
            if figure == KNIGHT:
                return KNIGHT_VALUES_OPENING[63 - position]
            if figure == BISHOP:
                return BISHOP_VALUES_OPENING[63 - position]
            if figure == QUEEN:
                return QUEEN_VALUES_OPENING[63 - position]
            if figure == ROOK:
                return ROOK_VALUES_OPENING[63 - position]
            if figure == KING:
                return KING_VALUES_OPENING[63 - position]
        if player == BLACK:
            if figure == PAWN:
                return PAWN_VALUES_OPENING[position]
            if figure == KNIGHT:
                return KNIGHT_VALUES_OPENING[position]
            if figure == BISHOP:
                return BISHOP_VALUES_OPENING[position]
            if figure == QUEEN:
                return QUEEN_VALUES_OPENING[position]
            if figure == ROOK:
                return ROOK_VALUES_OPENING[position]
            if figure == KING:
                return KING_VALUES_OPENING[position]
    if game_phase == "midgame":
        if player == WHITE:
            if figure == PAWN:
                return PAWN_VALUES_MIDGAME[63 - position]
            if figure == KNIGHT:
                return KNIGHT_VALUES_MIDGAME[63 - position]
            if figure == BISHOP:
                return BISHOP_VALUES_MIDGAME[63 - position]
            if figure == QUEEN:
                return QUEEN_VALUES_MIDGAME[63 - position]
            if figure == ROOK:
                return ROOK_VALUES_MIDGAME[63 - position]
            if figure == KING:
                return KING_VALUES_MIDGAME[63 - position]
        if player == BLACK:
            if figure == PAWN:
                return PAWN_VALUES_MIDGAME[position]
            if figure == KNIGHT:
                return KNIGHT_VALUES_MIDGAME[position]
            if figure == BISHOP:
                return BISHOP_VALUES_MIDGAME[position]
            if figure == QUEEN:
                return QUEEN_VALUES_MIDGAME[position]
            if figure == ROOK:
                return ROOK_VALUES_MIDGAME[position]
            if figure == KING:
                return KING_VALUES_MIDGAME[position]
    if game_phase == "endgame":
        if player == WHITE:
            if figure == PAWN:
                return PAWN_VALUES_ENDGAME[63 - position]
            if figure == KNIGHT:
                return KNIGHT_VALUES_ENDGAME[63 - position]
            if figure == BISHOP:
                return BISHOP_VALUES_ENDGAME[63 - position]
            if figure == QUEEN:
                return QUEEN_VALUES_ENDGAME[63 - position]
            if figure == ROOK:
                return ROOK_VALUES_ENDGAME[63 - position]
            if figure == KING:
                return KING_VALUES_ENDGAME[63 - position]
        if player == BLACK:
            if figure == PAWN:
                return PAWN_VALUES_ENDGAME[position]
            if figure == KNIGHT:
                return KNIGHT_VALUES_ENDGAME[position]
            if figure == BISHOP:
                return BISHOP_VALUES_ENDGAME[position]
            if figure == QUEEN:
                return QUEEN_VALUES_ENDGAME[position]
            if figure == ROOK:
                return ROOK_VALUES_ENDGAME[position]
            if figure == KING:
                return KING_VALUES_ENDGAME[position]
            
    logger.error("Error in get_figure_value().")
        

if __name__ == "__main__":
    value = get_figure_value(BLACK, 55, PAWN, game_phase= "midgame")
    print(value)
