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


def get_pawn_moves(bitboards, current_player):
    empty_squares = ~(bitboards[WHITE] | bitboards[BLACK])
    pawn_moves = []

    if current_player == WHITE:
        one_step = (bitboards[PAWN] & bitboards[WHITE]) << 8 & empty_squares
        two_steps = ((one_step & 0x000000000000FF00) << 8) & empty_squares
        captures_left = (bitboards[PAWN] & bitboards[WHITE]) << 7 & bitboards[BLACK] & ~0x8080808080808080
        captures_right = (bitboards[PAWN] & bitboards[WHITE]) << 9 & bitboards[BLACK] & ~0x0101010101010101
    else:
        one_step = (bitboards[PAWN] & bitboards[BLACK]) >> 8 & empty_squares
        two_steps = ((one_step & 0x00FF000000000000) >> 8) & empty_squares
        captures_left = (bitboards[PAWN] & bitboards[BLACK]) >> 9 & bitboards[WHITE] & ~0x8080808080808080
        captures_right = (bitboards[PAWN] & bitboards[BLACK]) >> 7 & bitboards[WHITE] & ~0x0101010101010101

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



def get_knight_moves(bitboards, current_player):
    # TODO: Implement knight move generation
    return []


def get_bishop_moves(bitboards, current_player):
    # TODO: Implement bishop move generation
    return []


def get_rook_moves(bitboards, current_player):
    # TODO: Implement rook move generation
    return []


def get_queen_moves(bitboards, current_player):
    # TODO: Implement queen move generation
    return []


def get_king_moves(bitboards, current_player):
    # TODO: Implement king move generation
    return []


def is_move_legal(move, bitboards, current_player):
    # TODO: Implement legality check for the given move
    return []


def generate_legal_moves(bitboards, current_player):
    moves = []

    moves += get_pawn_moves(bitboards, current_player)
    moves += get_knight_moves(bitboards, current_player)
    moves += get_bishop_moves(bitboards, current_player)
    moves += get_rook_moves(bitboards, current_player)
    moves += get_queen_moves(bitboards, current_player)
    moves += get_king_moves(bitboards, current_player)

    legal_moves = [move for move in moves if is_move_legal(move, bitboards, current_player)]

    return legal_moves

def print_legal_moves(bitboards, current_player):
    legal_moves = generate_legal_moves(bitboards, current_player)
    print("Legal moves for the current player ({}):".format("White" if current_player == WHITE else "Black"))
    for move in legal_moves:
        print(move)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    current_player = 'WHITE'
    bitboards = initialize_bitboards()
    # print_board(bitboards)
    # print_bitboards(bitboards)
    print_legal_moves(bitboards, current_player)
