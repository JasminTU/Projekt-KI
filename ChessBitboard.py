from loguru import logger


class ChessBitboard:
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

    def __init__(self):
        self.bitboards = self.initialize_bitboards()
        self.current_player = self.WHITE

    # Define bitmasks for the edges of the board
    RIGHT_EDGE = int("0b0111111101111111011111110111111101111111011111110111111101111111", 2)
    LEFT_EDGE = int("0b1111111011111110111111101111111011111110111111101111111011111110", 2)
    BOTH_EDGES = RIGHT_EDGE & (RIGHT_EDGE << 1)
    # for bitwise inversion
    MAX_VALUE = int("0b1111111111111111111111111111111111111111111111111111111111111111", 2)

    def initialize_bitboards(self):
        bitboards = [0] * 8

        # Set initial positions for white, black and all pieces using binary literals
        bitboards[self.WHITE] = int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
        bitboards[self.BLACK] = int("0b1111111111111111000000000000000000000000000000000000000000000000", 2)
        bitboards[self.PAWN] = int("0b0000000011111111000000000000000000000000000000001111111100000000", 2)
        bitboards[self.KNIGHT] = int("0b0100001000000000000000000000000000000000000000000000000001000010", 2)
        bitboards[self.BISHOP] = int("0b0010010000000000000000000000000000000000000000000000000000100100", 2)
        bitboards[self.ROOK] = int("0b1000000100000000000000000000000000000000000000000000000010000001", 2)
        bitboards[self.QUEEN] = int("0b0000100000000000000000000000000000000000000000000000000000001000", 2)
        bitboards[self.KING] = int("0b0001000000000000000000000000000000000000000000000000000000010000", 2)

        return bitboards

    def load_from_fen(self, fen):
        fen_parts = fen.split(" ")
        piece_positions = fen_parts[0]
        current_player_fen = fen_parts[1]

        self.current_player = self.WHITE if current_player_fen == "w" else self.BLACK

        rows = piece_positions.split("/")

        self.bitboards = [0] * 8

        piece_symbols = {
            "P": self.PAWN,
            "N": self.KNIGHT,
            "B": self.BISHOP,
            "R": self.ROOK,
            "Q": self.QUEEN,
            "K": self.KING,
        }

        # Process rows in reverse order
        for row_index, row in enumerate(reversed(rows)):
            col_index = 0
            for char in row:
                if char.isdigit():
                    col_index += int(char)
                else:
                    color = self.WHITE if char.isupper() else self.BLACK
                    piece_type = piece_symbols[char.upper()]

                    square = 1 << (row_index * 8 + col_index)

                    self.bitboards[color] |= square
                    self.bitboards[piece_type] |= square

                    col_index += 1


    def print_board(self, bitboards):
        piece_symbols = {
            (self.WHITE, self.PAWN): "P",
            (self.WHITE, self.KNIGHT): "N",
            (self.WHITE, self.BISHOP): "B",
            (self.WHITE, self.ROOK): "R",
            (self.WHITE, self.QUEEN): "Q",
            (self.WHITE, self.KING): "K",
            (self.BLACK, self.PAWN): "p",
            (self.BLACK, self.KNIGHT): "n",
            (self.BLACK, self.BISHOP): "b",
            (self.BLACK, self.ROOK): "r",
            (self.BLACK, self.QUEEN): "q",
            (self.BLACK, self.KING): "k",
        }

        # ANSI escape codes for formatting
        BOLD = '\033[1m'
        END = '\033[0m'

        for row in reversed(range(self.BOARD_SIZE)):
            for col in range(self.BOARD_SIZE):
                square = 1 << (row * self.BOARD_SIZE + col)
                piece = None
                color = (
                    self.WHITE
                    if bitboards[self.WHITE] & square
                    else self.BLACK
                    if bitboards[self.BLACK] & square
                    else None
                )

                if color is not None:
                    for piece_type in range(self.PAWN, self.KING + 1):
                        if bitboards[piece_type] & square:
                            piece = piece_symbols[(color, piece_type)]
                            break

                print(piece if piece else ".", end=" ")
            print(f"{BOLD} | {8 - row}{END}")
        print(f"{BOLD}-" * 15)
        print(f"a b c d e f g h{END}")

    def print_bitboards(self, bitboards):
        labels = {
            self.WHITE: "White",
            self.BLACK: "Black",
            self.PAWN: "Pawns",
            self.KNIGHT: "Knights",
            self.BISHOP: "Bishops",
            self.ROOK: "Rooks",
            self.QUEEN: "Queens",
            self.KING: "Kings",
        }

        for i, bitboard in enumerate(bitboards):
            print(labels[i] + ":")
            for row in reversed(range(self.BOARD_SIZE)):
                for col in range(self.BOARD_SIZE):
                    square = 1 << (row * self.BOARD_SIZE + col)
                    print("1" if bitboard & square else "0", end=" ")
                print()
            print()

    def move_to_algebraic(self, from_square, to_square):
        from_field = self.field_to_algebraic(from_square)
        to_field = self.field_to_algebraic(to_square)

        return f"{from_field}{to_field}"

    def field_to_algebraic(self, field):
        col_names = "abcdefgh"
        row_names = "12345678"

        col = col_names[(field.bit_length() - 1) % 8]
        row = row_names[(field.bit_length() - 1) // 8]

        return f"{col}{row}"

    def algebraic_to_field(self, algebraic):
        col_names = "abcdefgh"
        row_names = "12345678"

        col = algebraic[0]
        row = algebraic[1]

        col_index = col_names.index(col)
        row_index = row_names.index(row)

        field = 1 << (row_index * 8 + col_index)

        return field

    def algebraic_to_move(self, move):
        from_algebraic = move[0:2]
        to_algebraic = move[2:4]

        from_square = self.algebraic_to_field(from_algebraic)
        to_square = self.algebraic_to_field(to_algebraic)

        return (from_square, to_square)

    def get_pawn_moves(self, bitboards, current_player):
        empty_squares = ~(bitboards[self.WHITE] | bitboards[self.BLACK])
        pawn_moves = []

        white_pawn_bitboard = int(
            "0b0000000000000000000000000000000000000000000000001111111100000000", 2
        )
        black_pawn_bitboard = int(
            "0b0000000011111111000000000000000000000000000000000000000000000000", 2
        )

        if current_player == self.WHITE:
            one_step = (bitboards[self.PAWN] & bitboards[self.WHITE]) << 8 & empty_squares
            two_steps = ((bitboards[self.PAWN] & white_pawn_bitboard) << 16) & empty_squares
            captures_left = (bitboards[self.PAWN] & bitboards[self.WHITE]) << 7 & bitboards[self.BLACK]
            captures_right = (bitboards[self.PAWN] & bitboards[self.WHITE]) << 9 & bitboards[self.BLACK]
        else:
            one_step = (bitboards[self.PAWN] & bitboards[self.BLACK]) >> 8 & empty_squares
            two_steps = ((bitboards[self.PAWN] & black_pawn_bitboard) >> 16) & empty_squares
            captures_left = (bitboards[self.PAWN] & bitboards[self.BLACK]) >> 7 & bitboards[self.WHITE]
            captures_right = (bitboards[self.PAWN] & bitboards[self.BLACK]) >> 9 & bitboards[self.WHITE]

        moves = [
            (one_step, "one_step"),
            (two_steps, "two_steps"),
            (captures_left, "captures_left"),
            (captures_right, "captures_right"),
        ]

        for move_type in moves:
            move, move_name = move_type
            while move != 0:
                to_square = move & -move
                from_square = 0

                if move_name == "one_step":
                    from_square = (
                        to_square >> 8 if current_player == self.WHITE else to_square << 8
                    )

                if move_name == "two_steps":
                    from_square = (
                        to_square >> 16 if current_player == self.WHITE else to_square << 16
                    )

                if move_name == "captures_left":
                    from_square = (
                        to_square >> 7 if current_player == self.WHITE else to_square << 7
                    )

                if move_name == "captures_right":
                    from_square = (
                        to_square >> 9 if current_player == self.WHITE else to_square << 9
                    )

                pawn_moves.append((from_square, to_square))
                move &= move - 1

        return pawn_moves

    def get_knight_moves(self, board, player):
        # Define the bitboards for each player
        knights = board[player] & board[self.KNIGHT]
        occupied = board[player]
        empty = occupied ^ self.MAX_VALUE
        moves = []
        while knights:
            # Get the position of the least significant set bit (i.e., the position of the current knight)
            knight_pos = knights & -knights
            # Reihenfolge: Oben dia-links, links dia-oben, rechts dia-oben, oben dia-rechts, links dia-unten, unten dia-links, unten dia-rechts, rechts dia-unten
            knight_moves = (
                (((self.LEFT_EDGE & knight_pos) << 15) & empty),
                (((self.LEFT_EDGE & (self.LEFT_EDGE << 1) & knight_pos) << 6) & empty),
                (((self.RIGHT_EDGE & (self.RIGHT_EDGE >> 1) & knight_pos) << 10) & empty),
                (((self.RIGHT_EDGE & knight_pos) << 17) & empty),
                (((self.LEFT_EDGE & (self.LEFT_EDGE << 1) & knight_pos) >> 10) & empty),
                (((self.LEFT_EDGE & knight_pos) >> 17) & empty),
                (((self.RIGHT_EDGE & knight_pos) >> 15) & empty),
                (((self.RIGHT_EDGE & (self.RIGHT_EDGE >> 1) & knight_pos) >> 6) & empty),
            )
            # Convert the bitboard positions to tuples and add them to the list of moves
            moves += [(knight_pos, dest) for dest in knight_moves if dest]

            # Clear the least significant set bit (i.e., remove the current knight from the bitboard)
            knights &= knights - 1
        return moves

    def print_bitboard(self, message, bitboard):
        # print a single bitboard in a 8x8 grid
        print(message, "\n")
        for row in range(7, -1, -1):
            for col in range(8):
                index = row * 8 + col
                if bitboard & (1 << index):
                    print("1", end=" ")
                else:
                    print("0", end=" ")
            print()
        print("--------\n")

    def get_figure_moves(self, bitboards, current_player, figure):
        figure_moves = []
        figures = bitboards[figure] & bitboards[current_player]

        while figures:
            from_square = figures & -figures
            if figure == self.ROOK:
                attacks = self.generate_rook_attacks(from_square,
                                                     bitboards[self.WHITE] if current_player != self.WHITE else
                                                     bitboards[self.BLACK], bitboards[current_player])
            elif figure == self.BISHOP:
                attacks = self.generate_bishop_attacks(from_square,
                                                       bitboards[self.WHITE] if current_player != self.WHITE else
                                                       bitboards[self.BLACK], bitboards[current_player])
            elif figure == self.QUEEN:
                attacks = self.generate_rook_attacks(from_square,
                                                     bitboards[self.WHITE] if current_player != self.WHITE else
                                                     bitboards[self.BLACK], bitboards[current_player])
                attacks |= self.generate_bishop_attacks(from_square,
                                                        bitboards[self.WHITE] if current_player != self.WHITE else
                                                        bitboards[self.BLACK], bitboards[current_player])
            else:
                logger.error("Unknown figure: ", figure)

            while attacks:
                to_square = attacks & -attacks
                figure_moves.append((from_square, to_square))
                attacks &= attacks - 1

            figures &= figures - 1

        return figure_moves

    def generate_bishop_attacks(self, square, opp_occupied_squares, player_occupied_squares):
        attacks = 0
        attack_directions = [-9, -7, 7, 9]

        for direction in attack_directions:
            possible_square = square
            while True:
                possible_square = (possible_square << direction if direction > 0 else possible_square >> -direction)
                # Check if the square is within the board
                if not (0 <= possible_square.bit_length() - 1 < 64):
                    break
                if possible_square & opp_occupied_squares:  # Stop if the square is occupied
                    attacks |= possible_square
                    break
                if possible_square & player_occupied_squares:
                    break
                # print_bitboard("Possible Sq: ", possible_square)
                attacks |= possible_square
                if (direction in [-9, 7] and (self.LEFT_EDGE & possible_square) == 0) or (
                    direction in [-7, 9] and (self.RIGHT_EDGE & possible_square) == 0):
                    break
        return attacks

    def generate_rook_attacks(self, square, opp_occupied_squares, player_occupied_squares):
        attacks = 0
        attack_directions = [-8, -1, 1, 8]

        for direction in attack_directions:
            possible_square = square
            while True:
                possible_square = (possible_square << direction if direction > 0 else possible_square >> -direction)
                # Check if the square is within the board
                if not (0 <= possible_square.bit_length() - 1 < 64):
                    break
                if possible_square & opp_occupied_squares:  # Stop if the square is occupied
                    attacks |= possible_square
                    break
                if possible_square & player_occupied_squares:
                    break
                attacks |= possible_square
                if (direction == -1 and (self.LEFT_EDGE & possible_square) == 0) or (
                    direction == 1 and (self.RIGHT_EDGE & possible_square) == 0):
                    break
        return attacks

    def get_king_moves(self, bitboards, current_player):
        king_moves = []
        king_attack_offsets = (-9, -8, -7, -1, 1, 7, 8, 9)
        king = bitboards[self.KING] & bitboards[current_player]

        while king:
            from_square = king & -king
            for offset in king_attack_offsets:
                to_square = from_square << offset if offset > 0 else from_square >> -offset
                # Check if the move is within the board
                if not to_square or to_square.bit_length() > 63:
                    continue
                # Check if the move captures an opponent's piece or is an empty square
                if to_square & bitboards[current_player] != 0:
                    continue
                king_moves.append((from_square, to_square))
            king &= king - 1
        return king_moves

    def is_move_legal(self, move, bitboards, current_player):
        # For now, let's assume all generated moves are legal.
        # This does not account for more complex rules such as king's safety and en passant, which can be added later.
        return True

    def generate_legal_moves(self, bitboards, current_player):
        moves = []

        moves += self.get_pawn_moves(bitboards, current_player)
        # moves += self.get_knight_moves(bitboards, current_player)
        # moves += self.get_figure_moves(bitboards, current_player, self.BISHOP)
        # moves += self.get_figure_moves(bitboards, current_player, self.ROOK)
        # moves += self.get_figure_moves(bitboards, current_player, self.QUEEN)
        # moves += self.get_king_moves(bitboards, current_player)

        legal_moves = [
            move for move in moves if self.is_move_legal(move, bitboards, self.current_player)
        ]

        return legal_moves

    def perform_move(self, move_algebraic):
        move = self.algebraic_to_move(move_algebraic)
        legal_moves = self.generate_legal_moves(self.bitboards, self.current_player)
        if move not in legal_moves:
            raise Exception("Illegal move: ", move_algebraic)
        from_square, to_square = move
        if self.bitboards[self.WHITE] & from_square:
            if self.current_player == self.BLACK:
                raise Exception("Illegal move: ", move_algebraic, ". Current player: ", self.current_player, "but move is for white")
            self.bitboards[self.WHITE] &= ~from_square
            self.bitboards[self.WHITE] |= to_square
        if self.bitboards[self.BLACK] & from_square:
            if self.current_player == self.WHITE:
                raise Exception("Illegal move: ", move_algebraic, ". Current player: ", self.current_player, "but move is for black")
            self.bitboards[self.BLACK] &= ~from_square
            self.bitboards[self.BLACK] |= to_square
        for piece in range(2, 8):
            if self.bitboards[piece] & from_square:
                self.bitboards[piece] &= ~from_square
                self.bitboards[piece] |= to_square
                break
        self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK

    def print_legal_moves(self, bitboards, current_player):
        legal_moves = self.generate_legal_moves(bitboards, current_player)
        print(
            "\nLegal moves for the current player ({}):".format(
                "White" if current_player == self.WHITE else "Black"
            )
        )
        for move in legal_moves:
            from_square, to_square = move
            print(self.move_to_algebraic(from_square, to_square))


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    chessBitboard = ChessBitboard()


    # #Set initial positions for white pieces using binary literals
    # bitboards[WHITE] =  int("0b0000100000000000000000000000000000000000001000000010000000000101", 2)
    # bitboards[KING] =   int("0b0000100000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[PAWN] =   int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[KNIGHT] = int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[BISHOP] = int("0b0000000000000000000000000000000000000000001000000000000000000101", 2)
    # bitboards[ROOK] =   int("0b0000000000000000000000000000000000000000000000000010000000000000", 2)
    # bitboards[QUEEN] =  int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)

    # # Set initial positions for black pieces using binary literals
    # bitboards[BLACK] =   int("0b0000000000000001000000000000000001000000000000000000100000000000", 2)
    # bitboards[KNIGHT] |= int("0b0000000000000001000000000000000001000000000000000000100000000000", 2)
    # bitboards[PAWN] |=   int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[BISHOP] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[ROOK] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[QUEEN] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[KING] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # print_board(bitboards)

    chessBitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2")
    chessBitboard.perform_move("e2e4")
    chessBitboard.print_bitboards(chessBitboard.bitboards)
    chessBitboard.print_board(chessBitboard.bitboards)
    chessBitboard.print_legal_moves(chessBitboard.bitboards, chessBitboard.current_player)
