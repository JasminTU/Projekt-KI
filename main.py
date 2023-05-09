from loguru import logger
import sys


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

    # Set initial positions for white pieces using binary literals
    bitboards[WHITE] = int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
    bitboards[PAWN] = int("0b0000000000000000000000000000000000000000000000001111111100000000", 2)
    bitboards[KNIGHT] = int("0b0000000000000000000000000000000000000000000000000000000001000010", 2)
    bitboards[BISHOP] = int("0b00000000000000000000000000000000000000000000000000000000000100100", 2)
    bitboards[ROOK] = int("0b0000000000000000000000000000000000000000000000000000000010000001", 2)
    bitboards[QUEEN] = int("0b0000000000000000000000000000000000000000000000000000000000001000", 2)
    bitboards[KING] = int("0b0000000000000000000000000000000000000000000000000000000000010000", 2)

    # Set initial positions for black pieces using binary literals
    bitboards[BLACK] = int("0b1111111111111111000000000000000000000000000000000000000000000000", 2)
    bitboards[PAWN] |= int("0b0000000011111111000000000000000000000000000000000000000000000000", 2)
    bitboards[KNIGHT] |= int("0b0100001000000000000000000000000000000000000000000000000000000000", 2)
    bitboards[BISHOP] |= int("0b0010010000000000000000000000000000000000000000000000000000000000", 2)
    bitboards[ROOK] |= int("0b1000000100000000000000000000000000000000000000000000000000000000", 2)
    bitboards[QUEEN] |= int("0b0000100000000000000000000000000000000000000000000000000000000000", 2)
    bitboards[KING] |= int("0b0001000000000000000000000000000000000000000000000000000000000000", 2)

    return bitboards


def fen_to_bitboards(fen):
    fen_parts = fen.split(" ")
    piece_positions = fen_parts[0]
    current_player_fen = fen_parts[1]

    current_player = WHITE if current_player_fen == 'w' else BLACK

    rows = piece_positions.split("/")

    bitboards = [0] * 8

    piece_symbols = {
        'P': PAWN,
        'N': KNIGHT,
        'B': BISHOP,
        'R': ROOK,
        'Q': QUEEN,
        'K': KING
    }

    for row_index, row in enumerate(reversed(rows)):  # Process rows in reverse order
        col_index = 0
        for char in row:
            if char.isdigit():
                col_index += int(char)
            else:
                color = WHITE if char.isupper() else BLACK
                piece_type = piece_symbols[char.upper()]

                square = 1 << (row_index * 8 + col_index)

                bitboards[color] |= square
                bitboards[piece_type] |= square

                col_index += 1

    return bitboards, current_player


def print_board(bitboards):
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


def move_to_algebraic(from_square, to_square):
    from_field = field_to_algebraic(from_square)
    to_field = field_to_algebraic(to_square)

    return f"{from_field}{to_field}"


def field_to_algebraic(field):
    col_names = "abcdefgh"
    row_names = "12345678"

    col = col_names[(field.bit_length() - 1) % 8]
    row = row_names[(field.bit_length() - 1) // 8]

    return f"{col}{row}"


def algebraic_to_field(algebraic):
    col_names = "abcdefgh"
    row_names = "12345678"

    col = algebraic[0]
    row = algebraic[1]

    col_index = col_names.index(col)
    row_index = row_names.index(row)

    field = 1 << (row_index * 8 + col_index)

    return field

def algebraic_to_move(move):
    from_algebraic = move[0:2]
    to_algebraic = move[2:4]

    from_square = algebraic_to_field(from_algebraic)
    to_square = algebraic_to_field(to_algebraic)

    return (from_square, to_square)


def get_pawn_moves(bitboards, current_player):
    empty_squares = ~(bitboards[WHITE] | bitboards[BLACK])
    pawn_moves = []

    white_pawn_bitboard = int("0b0000000000000000000000000000000000000000000000001111111100000000", 2)
    black_pawn_bitboard = int("0b0000000011111111000000000000000000000000000000000000000000000000", 2)

    if current_player == WHITE:
        one_step = (bitboards[PAWN] & bitboards[WHITE]) << 8 & empty_squares
        two_steps = ((bitboards[PAWN] & white_pawn_bitboard) << 16) & empty_squares
        captures_left = (bitboards[PAWN] & bitboards[WHITE]) << 7 & bitboards[BLACK]
        captures_right = (bitboards[PAWN] & bitboards[WHITE]) << 9 & bitboards[BLACK]
    else:
        one_step = (bitboards[PAWN] & bitboards[BLACK]) >> 8 & empty_squares
        two_steps = ((bitboards[PAWN] & black_pawn_bitboard) >> 16) & empty_squares
        captures_left = (bitboards[PAWN] & bitboards[BLACK]) >> 9 & bitboards[WHITE]
        captures_right = (bitboards[PAWN] & bitboards[BLACK]) >> 7 & bitboards[WHITE]

    moves = [(one_step, 'one_step'), (two_steps, 'two_steps'), (captures_left, 'captures_left'), (captures_right, 'captures_right')]

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
    moves = []

    while knights:
        print("haha")
        # Get the position of the least significant set bit (i.e., the position of the current knight)
        print_bitboard("Before shifting: ", knights & -knights)
        knight_pos = knights & -knights
        # Reihenfolge: Oben dia-links, links dia-oben, rechts dia-oben, oben dia-rechts, links dia-unten, unten dia-links, unten dia-rechts, rechts dia-unten
        knight_moves = ((((LEFT_EDGE & knight_pos) << 15) & empty),
                        (((LEFT_EDGE & (LEFT_EDGE << 1) & knight_pos) << 6) & empty),
                        (((RIGHT_EDGE & (RIGHT_EDGE >> 1) & knight_pos) << 10) & empty),
                        (((RIGHT_EDGE & knight_pos) << 17) & empty),
                        (((LEFT_EDGE & (LEFT_EDGE << 1) & knight_pos) >> 10) & empty),
                        (((LEFT_EDGE & knight_pos) >> 17) & empty),
                        (((RIGHT_EDGE & knight_pos) >> 15) & empty),
                        (((RIGHT_EDGE & (RIGHT_EDGE >> 1) & knight_pos) >> 6) & empty))
        # Convert the bitboard positions to tuples and add them to the list of moves
        moves += [(knight_pos, dest) for dest in knight_moves if dest]

        # Clear the least significant set bit (i.e., remove the current knight from the bitboard)
        knights &= knights - 1
    return moves


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
    pass


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

    # moves += get_pawn_moves(bitboards, current_player)
    moves += get_knight_moves(bitboards, current_player)
    # moves += get_bishop_moves(bitboards, current_player)
    # moves += get_rook_moves(bitboards, current_player)
    # moves += get_queen_moves(bitboards, current_player)
    # moves += get_king_moves(bitboards, current_player)

    legal_moves = [move for move in moves if is_move_legal(
        move, bitboards, current_player)]

    return legal_moves


def print_legal_moves(bitboards, current_player):
    legal_moves = generate_legal_moves(bitboards, current_player)
    print("Legal moves for the current player ({}):".format(
        "White" if current_player == WHITE else "Black"))
    for move in legal_moves:
        from_square, to_square = move
        print(move_to_algebraic(from_square, to_square))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    current_player = WHITE
    bitboards = initialize_bitboards()
    print_board(bitboards)
    # print_bitboards(bitboards)
    # available_moves = get_knight_moves(bitboards, current_player)
    # print_bitboard("Final bitboard", available_moves)
    # print_legal_moves(bitboards, current_player)

    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position in FEN notation
    bitboards, current_player = fen_to_bitboards(fen)

    print_board(bitboards)
    print("Current player:", "White" if current_player == WHITE else "Black")

