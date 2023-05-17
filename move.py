from loguru import logger
from illegalMoveException import IllegalMoveException
from PrintBitboardService import PrintBitBoardService
import constants
from collections import Counter
import copy

# Define bitmasks for the edges of the board
NOT_RIGHT_EDGE = int("0b0111111101111111011111110111111101111111011111110111111101111111", 2)
NOT_LEFT_EDGE = int("0b1111111011111110111111101111111011111110111111101111111011111110", 2)
NOT_EDGES = NOT_RIGHT_EDGE & (NOT_RIGHT_EDGE << 1)
MAX_VALUE = int("0b1111111111111111111111111111111111111111111111111111111111111111", 2)  # for bitwise inversion


class Move():

    def __init__(self):
        pass

    def get_pawn_moves(self, bitboards, current_player):
        empty_squares = ~(bitboards[constants.WHITE] | bitboards[constants.BLACK])
        pawn_moves = []

        white_pawn_bitboard = int(
            "0b0000000000000000000000000000000000000000000000001111111100000000", 2
        )
        black_pawn_bitboard = int(
            "0b0000000011111111000000000000000000000000000000000000000000000000", 2
        )

        if current_player == constants.WHITE:
            one_step = (bitboards[constants.PAWN] & bitboards[constants.WHITE]) << 8 & empty_squares
            two_steps = ((bitboards[constants.PAWN] & white_pawn_bitboard) << 16) & empty_squares
            captures_left = (bitboards[constants.PAWN] & bitboards[constants.WHITE] & NOT_LEFT_EDGE) << 7 & bitboards[
                constants.BLACK]
            captures_right = (bitboards[constants.PAWN] & bitboards[constants.WHITE] & NOT_RIGHT_EDGE) << 9 & bitboards[
                constants.BLACK]
        else:
            one_step = (bitboards[constants.PAWN] & bitboards[constants.BLACK]) >> 8 & empty_squares
            two_steps = ((bitboards[constants.PAWN] & black_pawn_bitboard) >> 16) & empty_squares
            captures_left = (bitboards[constants.PAWN] & bitboards[constants.BLACK] & NOT_LEFT_EDGE) >> 9 & bitboards[
                constants.WHITE]
            captures_right = (bitboards[constants.PAWN] & bitboards[constants.BLACK] & NOT_RIGHT_EDGE) >> 7 & bitboards[
                constants.WHITE]

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
                        to_square >> 8 if current_player == constants.WHITE else to_square << 8
                    )

                if move_name == "two_steps":
                    from_square = (
                        to_square >> 16 if current_player == constants.WHITE else to_square << 16
                    )

                if move_name == "captures_left":
                    from_square = (
                        to_square >> 7 if current_player == constants.WHITE else to_square << 9
                    )

                if move_name == "captures_right":
                    from_square = (
                        to_square >> 9 if current_player == constants.WHITE else to_square << 7
                    )

                pawn_moves.append((from_square, to_square))
                move &= move - 1

        return pawn_moves

    def _get_knight_moves(self, board, player):
        # Define the bitboards for each player
        knights = board[player] & board[constants.KNIGHT]
        occupied = board[player]
        empty = occupied ^ MAX_VALUE
        moves = []
        while knights:
            # Get the position of the least significant set bit (i.e., the position of the current constants.KNIGHT)
            knight_pos = knights & -knights
            # Reihenfolge: Oben dia-links, links dia-oben, rechts dia-oben, oben dia-rechts, links dia-unten, unten dia-links, unten dia-rechts, rechts dia-unten
            knight_moves = (
                (((NOT_LEFT_EDGE & knight_pos) << 15) & empty),
                (((NOT_LEFT_EDGE & (NOT_LEFT_EDGE << 1) & knight_pos) << 6) & empty),
                (((NOT_RIGHT_EDGE & (NOT_RIGHT_EDGE >> 1) & knight_pos) << 10) & empty),
                (((NOT_RIGHT_EDGE & knight_pos) << 17) & empty),
                (((NOT_LEFT_EDGE & (NOT_LEFT_EDGE << 1) & knight_pos) >> 10) & empty),
                (((NOT_LEFT_EDGE & knight_pos) >> 17) & empty),
                (((NOT_RIGHT_EDGE & knight_pos) >> 15) & empty),
                (((NOT_RIGHT_EDGE & (NOT_RIGHT_EDGE >> 1) & knight_pos) >> 6) & empty),
            )
            # Convert the bitboard positions to tuples and add them to the list of moves
            moves += [(knight_pos, dest) for dest in knight_moves if dest]

            # Clear the least significant set bit (i.e., remove the current constants.KNIGHT from the bitboard)
            knights &= knights - 1
        return moves

    def _generate_bishop_attacks(self, square, opp_occupied_squares, player_occupied_squares):
        attacks = 0
        attack_directions = [-9, -7, 7, 9]

        for direction in attack_directions:
            possible_square = square
            while True:
                if (direction in [-9, 7] and (NOT_LEFT_EDGE & possible_square) == 0) or (
                    direction in [-7, 9] and (NOT_RIGHT_EDGE & possible_square) == 0):
                    break
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
        return attacks

    def _generate_rook_attacks(self, square, opp_occupied_squares, player_occupied_squares):
        attacks = 0
        attack_directions = [-8, -1, 1, 8]

        for direction in attack_directions:
            possible_square = square
            while True:
                if (direction == -1 and (NOT_LEFT_EDGE & possible_square) == 0) or (
                    direction == 1 and (NOT_RIGHT_EDGE & possible_square) == 0):
                    break
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
        return attacks

    def _get_king_moves(self, bitboards, current_player):
        king_moves = []
        king_attack_offsets = (-9, -8, -7, -1, 1, 7, 8, 9)
        king_position = bitboards[constants.KING] & bitboards[current_player]

        while king_position:
            from_square = king_position & -king_position
            for offset in king_attack_offsets:
                to_square = from_square << offset if offset > 0 else from_square >> -offset
                # Check if the move is within the board
                if (offset in [-9, 7, -1] and (NOT_LEFT_EDGE & from_square) == 0) or (
                    offset in [-7, 9, 1] and (NOT_RIGHT_EDGE & from_square) == 0):
                    continue
                if not to_square or to_square.bit_length() > 63:
                    continue
                # Check if the move captures an opponent's piece or is an empty square
                if to_square & bitboards[current_player] != 0:
                    continue
                king_moves.append((from_square, to_square))
            king_position &= king_position - 1
        return king_moves
    
    def get_move_by_figure(self, bitboards, current_player, figure):
        figure_moves = []
        figures = bitboards[figure] & bitboards[current_player]

        while figures:
            from_square = figures & -figures
            if figure == constants.ROOK:
                attacks = self._generate_rook_attacks(from_square,
                                                     bitboards[
                                                         constants.WHITE] if current_player != constants.WHITE else
                                                     bitboards[constants.BLACK], bitboards[current_player])
            elif figure == constants.BISHOP:
                attacks = self._generate_bishop_attacks(from_square,
                                                       bitboards[
                                                           constants.WHITE] if current_player != constants.WHITE else
                                                       bitboards[constants.BLACK], bitboards[current_player])
            elif figure == constants.QUEEN:
                attacks = self._generate_rook_attacks(from_square,
                                                     bitboards[
                                                         constants.WHITE] if current_player != constants.WHITE else
                                                     bitboards[constants.BLACK], bitboards[current_player])
                attacks |= self._generate_bishop_attacks(from_square,
                                                        bitboards[
                                                            constants.WHITE] if current_player != constants.WHITE else
                                                        bitboards[constants.BLACK], bitboards[current_player])
            elif figure == constants.KING:
                return self._get_king_moves(bitboards, current_player)
            elif figure == constants.PAWN:
                return self.get_pawn_moves(bitboards, current_player)
            elif figure == constants.KNIGHT:
                return self._get_knight_moves(bitboards, current_player)
            else:
                logger.error("Unknown figure: ", figure)

            while attacks:
                to_square = attacks & -attacks
                figure_moves.append((from_square, to_square))
                attacks &= attacks - 1

            figures &= figures - 1

        return figure_moves

    def perform_move(self, move, board, move_type="algebraic", with_validation=True):
        # TODO: Je nach Verwendung der Funktion würde ich hier nicht nochmal alle legalen moves generieren, da der ausgewählte move bereits legal ist --> Laufzeitverlängerung
        if move_type == "algebraic":
            move = self.algebraic_move_to_binary(move)
        if with_validation:
            legal_moves = self.filter_illegal_moves(board, self.generate_moves(board))
            if move not in legal_moves and move_type != "algebraic":
                raise IllegalMoveException(self.binary_move_to_algebraic(move[0], move[1]))
            if move not in legal_moves:
                raise IllegalMoveException(move)
        from_square, to_square = move
        opponent = board.get_opponent(board.current_player)

        if board.bitboards[board.current_player] & from_square:
            # Remove the moving piece from its original position
            board.bitboards[board.current_player] &= ~from_square
            # Remove a possibly captured piece from the destination
            board.bitboards[opponent] &= ~to_square
            # Move the piece to the new position
            board.bitboards[board.current_player] |= to_square

        for piece in range(constants.PAWN, constants.KING + 1):
            if board.bitboards[piece] & from_square:
                # Remove the moving piece from its original position
                board.bitboards[piece] &= ~from_square
                # Move the piece to the new position
                board.bitboards[piece] |= to_square
            # Remove a possibly captured piece from the destination
            else:
                board.bitboards[piece] &= ~to_square

        # Switch the current player
        board.current_player = opponent
        copied_chessBoard = copy.deepcopy(board)
        board.board_history.append(copied_chessBoard.bitboards)
        

    def is_draw(self, legal_moves, chessBitboard):
        # TODO: There is one more draw rule "50-Züge-Regel"
        if not legal_moves and not chessBitboard.is_in_check(chessBitboard.current_player):
            print("Draw by Patt!")
            chessBitboard.game_result = constants.WHITE if chessBitboard.current_player == constants.BLACK else constants.BLACK
            return True
        if self._is_repetition_draw(chessBitboard.board_history):
            print("Draw by repetition!")
            chessBitboard.game_result = constants.WHITE if chessBitboard.current_player == constants.BLACK else constants.BLACK
            return True
        return False

    def _is_repetition_draw(self, board_list):
        # Wenn in einer Schachpartie dreimal die exakt gleiche Stellung auf dem Brett auftritt, endet die Partie in einem Remis. 
        # Mit exakt ist gemeint, dass jeweils der gleiche Spieler am Zug sein muss. Optionen wie das Rochaderecht oder En passant müssen ebenfalls identisch sein.
        # TODO: include rochade, ...
        for sublist in board_list:
            # print(board_list.count(sublist))
            if board_list.count(sublist) > 2:
                return True
        return False

    def algebraic_move_to_binary(self, move):
        def algebraic_field_to_binary(algebraic):
            col_names = "abcdefgh"
            row_names = "12345678"

            col = algebraic[0]
            row = algebraic[1]

            col_index = col_names.index(col)
            row_index = row_names.index(row)

            field = 1 << (row_index * 8 + col_index)

            return field

        from_algebraic = move[0:2]
        to_algebraic = move[2:4]

        from_square = algebraic_field_to_binary(from_algebraic)
        to_square = algebraic_field_to_binary(to_algebraic)

        return (from_square, to_square)

    @staticmethod
    def is_move_legal(move, board):
        board_after_move = copy.deepcopy(board)
        board_after_move.chess_move.perform_move(move, board_after_move, move_type="binary", with_validation=False)
        is_in_check = board_after_move.is_in_check(board.current_player)
        return not is_in_check

    def filter_illegal_moves(self, board, moves):
        # TODO: this seems a bit inefficient, I would rather select the best possible move and check if it is illgeal than filter all illegal moves
        legal_moves = [
            move for move in moves if self.is_move_legal(move, board)
        ]

        return legal_moves
    
    def generate_moves(self, board):
        moves = []
        moves += self.get_move_by_figure(board.bitboards, board.current_player, constants.PAWN)
        moves += self.get_move_by_figure(board.bitboards, board.current_player, constants.KNIGHT)
        moves += self.get_move_by_figure(board.bitboards, board.current_player, constants.BISHOP)
        moves += self.get_move_by_figure(board.bitboards, board.current_player, constants.ROOK)
        moves += self.get_move_by_figure(board.bitboards, board.current_player, constants.QUEEN)
        moves += self.get_move_by_figure(board.bitboards, board.current_player, constants.KING)

        return moves


    def print_legal_moves(self, board):
        legal_moves = self.generate_moves(board)
        print(
            "\nLegal moves for the current player ({}):".format(
                "constants.WHITE" if board.current_player == constants.WHITE else "constants.BLACK"
            )
        )
        for move in legal_moves:
            from_square, to_square = move
            print(self.binary_move_to_algebraic(from_square, to_square))

    def binary_move_to_algebraic(self, from_square, to_square):
        def binary_field_to_algebraic(field):
            col_names = "abcdefgh"
            row_names = "12345678"

            col = col_names[(field.bit_length() - 1) % 8]
            row = row_names[(field.bit_length() - 1) // 8]

            return f"{col}{row}"

        from_field = binary_field_to_algebraic(from_square)
        to_field = binary_field_to_algebraic(to_square)

        return f"{from_field}{to_field}"
