from loguru import logger
import sys
import numpy as np

# Constants
BOARD_SIZE = 8
WHITE = 0
BLACK = 1
PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6
KING = 7
# Define bitmasks for the edges of the board
RIGHT_EDGE = int(
    "0b0111111101111111011111110111111101111111011111110111111101111111", 2)
LEFT_EDGE = int(
    "0b1111111011111110111111101111111011111110111111101111111011111110", 2)
BOTH_EDGES = RIGHT_EDGE & (RIGHT_EDGE << 1)
# for bitwise inversion
MAX_VALUE = int(
    "0b1111111111111111111111111111111111111111111111111111111111111111", 2)


def initialize_bitboards():
    bitboards = [0] * 8
    # TODO: Warum haben wir 14 Boards? 8 würden doch reichen, weil zB bitboards[ALL_PAWNs] & bitboards[WHITE] dasselbe ist wie momentan bitboards[PAWN]; außerdem überschreiben wir gerade die Einträge

    # Set initial positions for white pieces using binary literals
    bitboards[WHITE] = int(
        "0b0000000000000000000000000000000000001000000000000000000011111101", 2)
    # bitboards[PAWN] = int(
    #   "0b0000000000000000000000000000000000000000000000001111111100000000", 2)
    bitboards[PAWN] = int(
        "0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    bitboards[KNIGHT] = int(
        "0b0000000000000000000000000000000000001000000000000000000001000000", 2)
    bitboards[BISHOP] = int(
        "0b00000000000000000000000000000000000000000000000000000000000100100", 2)
    bitboards[ROOK] = int(
        "0b0000000000000000000000000000000000000000000000000000000010000001", 2)
    bitboards[QUEEN] = int(
        "0b0000000000000000000000000000000000000000000000000000000000001000", 2)
    bitboards[KING] = int(
        "0b0000000000000000000000000000000000000000000000000000000000010000", 2)

    # Set initial positions for black pieces using binary literals
    bitboards[BLACK] = int(
        "0b1111111111111111000000000000000000000000000000000000000000000000", 2)
    bitboards[PAWN] |= int(
        "0b0000000011111111000000000000000000000000000000000000000000000000", 2)
    bitboards[KNIGHT] |= int(
        "0b0100001000000000000000000000000000000000000000000000000000000000", 2)
    bitboards[BISHOP] |= int(
        "0b0010010000000000000000000000000000000000000000000000000000000000", 2)
    bitboards[ROOK] |= int(
        "0b1000000100000000000000000000000000000000000000000000000000000000", 2)
    bitboards[QUEEN] |= int(
        "0b0000100000000000000000000000000000000000000000000000000000000000", 2)
    bitboards[KING] |= int(
        "0b0001000000000000000000000000000000000000000000000000000000000000", 2)

    return bitboards


def print_board(bitboards):
    # TODO: Diese Funktion funktioniert nicht auf ein einzelnes board. Name irreführend? Ich habe provisorisch eine schlechte Funktion hinzugefügt die auf ein einzelnes board funktioniert
    piece_symbols = {
        (WHITE, PAWN): "P",
        (WHITE, KNIGHT): "N",
        (WHITE, BISHOP): "B",
        (WHITE, ROOK): "R",
        (WHITE, QUEEN): "Q",
        (WHITE, KING): "K",
        (BLACK, PAWN): "p",
        (BLACK, KNIGHT): "n",
        (BLACK, BISHOP): "b",
        (BLACK, ROOK): "r",
        (BLACK, QUEEN): "q",
        (BLACK, KING): "k",
    }

    for row in reversed(range(BOARD_SIZE)):
        for col in range(BOARD_SIZE):
            square = 1 << (row * BOARD_SIZE + col)
            piece = None
            color = WHITE if bitboards[WHITE] & square else BLACK if bitboards[BLACK] & square else None

            if color is not None:
                for piece_type in range(PAWN, KING + 1):
                    if bitboards[piece_type] & square:
                        piece = piece_symbols[(color, piece_type)]
                        break

            print(piece if piece else ".", end=" ")
        print()


def print_bitboards(bitboards):
    labels = {
        WHITE: "White",
        BLACK: "Black",
        PAWN: "Pawns",
        KNIGHT: "Knights",
        BISHOP: "Bishops",
        ROOK: "Rooks",
        QUEEN: "Queens",
        KING: "Kings",
    }

    for i, bitboard in enumerate(bitboards):
        print(labels[i] + ":")
        for row in reversed(range(BOARD_SIZE)):
            for col in range(BOARD_SIZE):
                square = 1 << (row * BOARD_SIZE + col)
                print("1" if bitboard & square else "0", end=" ")
            print()
        print()


def get_pawn_moves(bitboards, current_player):
    empty_squares = ~(bitboards[WHITE] | bitboards[BLACK])
    pawn_moves = []

    if current_player == WHITE:
        one_step = (bitboards[PAWN] & bitboards[WHITE]) << 8 & empty_squares
        two_steps = ((one_step & 0x000000000000FF00) << 8) & empty_squares
        captures_left = (bitboards[PAWN] & bitboards[WHITE]
                         ) << 7 & bitboards[BLACK] & ~0x8080808080808080
        captures_right = (bitboards[PAWN] & bitboards[WHITE]
                          ) << 9 & bitboards[BLACK] & ~0x0101010101010101
    else:
        one_step = (bitboards[PAWN] & bitboards[BLACK]) >> 8 & empty_squares
        two_steps = ((one_step & 0x00FF000000000000) >> 8) & empty_squares
        captures_left = (bitboards[PAWN] & bitboards[BLACK]
                         ) >> 9 & bitboards[WHITE] & ~0x8080808080808080
        captures_right = (bitboards[PAWN] & bitboards[BLACK]
                          ) >> 7 & bitboards[WHITE] & ~0x0101010101010101

    moves = [(one_step, 'one_step'), (two_steps, 'two_steps'),
             (captures_left, 'captures_left'), (captures_right, 'captures_right')]

    for move_type in moves:
        move, move_name = move_type
        while move != 0:
            to_square = move & -move
            from_square = to_square >> 8 if current_player == WHITE else to_square << 8

            if move_name == 'two_steps':
                from_square = from_square >> 8 if current_player == WHITE else from_square << 8

            if move_name == 'captures_left':
                from_square = from_square >> 7 if current_player == WHITE else from_square << 9

            if move_name == 'captures_right':
                from_square = from_square >> 9 if current_player == WHITE else from_square << 7

            pawn_moves.append((from_square, to_square))
            move &= move - 1

    return pawn_moves


def shift_by_direction(direction, number_fields):
    shift = None
    if direction == "north":
        shift = 1 << (8 * number_fields)
    if direction == "north_west":
        shift = 1 << (9 * number_fields)
    if direction == "north_east":
        shift = 1 << (7 * number_fields)
    if direction == "west":
        shift = 1 << number_fields
    if direction == "south":
        shift = 1 >> (8 * number_fields)
    if direction == "south_west":
        shift = 1 >> (7 * number_fields)
    if direction == "south_east":
        shift = 1 >> (9 * number_fields)
    if direction == "east":
        shift = 1 >> number_fields
    else:
        logger.error("Unknown direction:", direction)
        sys.exit(1)
    return shift


def get_knight_moves(board, player):
    # Define the bitboards for each player
    knights = board[player] & board[KNIGHT]
    occupied = board[WHITE] | board[BLACK]
    empty = occupied ^ MAX_VALUE

    print_bitboard("Before shifting: ", knights)
    print_bitboard("After shifting: ",
                   (((RIGHT_EDGE & (RIGHT_EDGE >> 1) & knights) >> 6) & empty))
    # Reihenfolge: Oben dia-links, links dia-oben, rechts dia-oben, oben dia-rechts, links dia-unten, unten dia-links, unten dia-rechts, rechts dia-unten
    return (((LEFT_EDGE & knights) << 15) & empty) | \
        (((LEFT_EDGE & (LEFT_EDGE << 1) & knights) << 6) & empty) | \
        (((RIGHT_EDGE & (RIGHT_EDGE >> 1) & knights) << 10) & empty) | \
        (((RIGHT_EDGE & knights) << 17) & empty) | \
        (((LEFT_EDGE & (LEFT_EDGE << 1) & knights) >> 10) & empty) | \
        (((LEFT_EDGE & knights) >> 17) & empty) | \
        (((RIGHT_EDGE & knights) >> 15) & empty) | \
        (((RIGHT_EDGE & (RIGHT_EDGE >> 1) & knights) >> 6) & empty)


def print_bitboard(message, bitboard):
    print(message, '\n')
    for row in range(7, -1, -1):
        for col in range(8):
            index = row * 8 + col
            if bitboard & (1 << index):
                print("1", end=" ")
            else:
                print("0", end=" ")
        print()
    print('--------\n')


def get_bishop_moves(bitboards, current_player):
    # TODO: Implement bishop move generation
    bishop_moves = []

    # Use bitwise operations to generate sliding moves for bishops
    def generate_bishop_attacks(square, occupied_squares):
        attacks = 0
        attack_directions = [-9, -7, 7, 9]

        for direction in attack_directions:
            possible_square = square
            while True:
                possible_square = (
                    possible_square << direction if direction > 0 else possible_square >> -direction)
                # Check if the square is within the board
                if not (0 <= possible_square.bit_length() - 1 < 64):
                    break
                if possible_square & occupied_squares:  # Stop if the square is occupied
                    attacks |= possible_square
                    break
                attacks |= possible_square

        return attacks

    bishops = bitboards[BISHOP] & bitboards[current_player]
    occupied_squares = bitboards[WHITE] | bitboards[BLACK]

    while bishops:
        from_square = bishops & -bishops
        attacks = generate_bishop_attacks(
            from_square, occupied_squares) & ~(bitboards[current_player])
        while attacks:
            to_square = attacks & -attacks
            bishop_moves.append((from_square, to_square))
            attacks &= attacks - 1

        bishops &= bishops - 1

    return bishop_moves


def get_rook_moves(bitboards, current_player):
    # TODO: Implement rook move generation
    rook_moves = []

    # Use bitwise operations to generate sliding moves for rooks
    def generate_rook_attacks(square, occupied_squares):
        attacks = 0
        attack_directions = [-8, -1, 1, 8]

        for direction in attack_directions:
            possible_square = square
            while True:
                possible_square = (
                    possible_square << direction if direction > 0 else possible_square >> -direction)
                # Check if the square is within the board
                if not (0 <= possible_square.bit_length() - 1 < 64):
                    break
                if possible_square & occupied_squares:  # Stop if the square is occupied
                    attacks |= possible_square
                    break
                attacks |= possible_square

        return attacks

    rooks = bitboards[ROOK] & bitboards[current_player]
    occupied_squares = bitboards[WHITE] | bitboards[BLACK]

    while rooks:
        from_square = rooks & -rooks
        attacks = generate_rook_attacks(from_square, occupied_squares)
        attacks &= ~(bitboards[current_player])
        while attacks:
            to_square = attacks & -attacks
            rook_moves.append((from_square, to_square))
            attacks &= attacks - 1

        rooks &= rooks - 1

    return rook_moves


def get_queen_moves(bitboards, current_player):
    # The queen's moves are RIGHT_EDGE combination of the bishop and rook moves
    return get_bishop_moves(bitboards, current_player) + get_rook_moves(bitboards, current_player)


def get_king_moves(bitboards, current_player):
    king_moves = []
    king_attack_offsets = (-9, -8, -7, -1, 1, 7, 8, 9)
    king = bitboards[KING] & bitboards[current_player]

    while king:
        from_square = king & -king
        for offset in king_attack_offsets:
            to_square = from_square << offset if offset > 0 else from_square >> -offset

            # Check if the move is within the board
            if to_square & (0xFFFFFFFFFFFFFFFF ^ (bitboards[WHITE] | bitboards[BLACK])) == 0:
                continue

            # Check if the move captures an opponent's piece or is an empty square
            if not (to_square & bitboards[1 - current_player]):
                continue

            king_moves.append((from_square, to_square))

        king &= king - 1

    return king_moves


def is_move_legal(move, bitboards, current_player):
    # For now, let's assume all generated moves are legal.
    # This does not account for more complex rules such as king's safety and en passant, which can be added later.
    return True


def generate_legal_moves(bitboards, current_player):
    moves = []

    moves += get_pawn_moves(bitboards, current_player)
    moves += get_knight_moves(bitboards, current_player)
    moves += get_bishop_moves(bitboards, current_player)
    moves += get_rook_moves(bitboards, current_player)
    moves += get_queen_moves(bitboards, current_player)
    moves += get_king_moves(bitboards, current_player)

    legal_moves = [move for move in moves if is_move_legal(
        move, bitboards, current_player)]

    return legal_moves


def print_legal_moves(bitboards, current_player):
    legal_moves = generate_legal_moves(bitboards, current_player)
    print("Legal moves for the current player ({}):".format(
        "White" if current_player == WHITE else "Black"))
    for move in legal_moves:
        print(move)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    current_player = WHITE
    bitboards = initialize_bitboards()
    print_board(bitboards)
    # print_bitboards(bitboards)
    available_moves = get_knight_moves(bitboards, current_player)
    print_bitboard("Final bitboard", available_moves)
    #print_legal_moves(bitboards, current_player)
