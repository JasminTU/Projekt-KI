from loguru import logger
from IllegalMoveException import IllegalMoveException
from ChessPrintService import ChessPrintService
import constants
from collections import Counter
import copy

from constants import NOT_RIGHT_EDGE, NOT_LEFT_EDGE


class ChessEngine():

    def __init__(self):
        pass

    @staticmethod
    def get_pawn_moves(board):
        empty_squares = ~(board.bitboards[constants.WHITE] | board.bitboards[constants.BLACK])
        pawn_moves = []

        white_pawn_bitboard = int(
            "0b0000000000000000000000000000000000000000000000001111111100000000", 2
        )
        black_pawn_bitboard = int(
            "0b0000000011111111000000000000000000000000000000000000000000000000", 2
        )

        if board.current_player == constants.WHITE:
            one_step = (board.bitboards[constants.PAWN] & board.bitboards[constants.WHITE]) << 8 & empty_squares
            two_steps = ((board.bitboards[constants.PAWN] & white_pawn_bitboard) << 16) & empty_squares
            captures_left = (board.bitboards[constants.PAWN] & board.bitboards[constants.WHITE] & NOT_LEFT_EDGE) << 7 & board.bitboards[
                constants.BLACK]
            captures_right = (board.bitboards[constants.PAWN] & board.bitboards[constants.WHITE] & NOT_RIGHT_EDGE) << 9 & board.bitboards[
                constants.BLACK]
        else:
            one_step = (board.bitboards[constants.PAWN] & board.bitboards[constants.BLACK]) >> 8 & empty_squares
            two_steps = ((board.bitboards[constants.PAWN] & black_pawn_bitboard) >> 16) & empty_squares
            captures_left = (board.bitboards[constants.PAWN] & board.bitboards[constants.BLACK] & NOT_LEFT_EDGE) >> 9 & board.bitboards[
                constants.WHITE]
            captures_right = (board.bitboards[constants.PAWN] & board.bitboards[constants.BLACK] & NOT_RIGHT_EDGE) >> 7 & board.bitboards[
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
                        to_square >> 8 if board.current_player == constants.WHITE else to_square << 8
                    )

                if move_name == "two_steps":
                    from_square = (
                        to_square >> 16 if board.current_player == constants.WHITE else to_square << 16
                    )

                if move_name == "captures_left":
                    from_square = (
                        to_square >> 7 if board.current_player == constants.WHITE else to_square << 9
                    )

                if move_name == "captures_right":
                    from_square = (
                        to_square >> 9 if board.current_player == constants.WHITE else to_square << 7
                    )

                pawn_moves.append((from_square, to_square))
                move &= move - 1

        return pawn_moves

    @staticmethod
    def _get_knight_moves(board):
        # Define the bitboards for each player
        knights = board.bitboards[board.current_player] & board.bitboards[constants.KNIGHT]
        occupied = board.bitboards[board.current_player]
        empty = occupied ^ constants.MAX_VALUE
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

    @staticmethod
    def _generate_bishop_attacks(square, opp_occupied_squares, player_occupied_squares):
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

    @staticmethod
    def _generate_rook_attacks(square, opp_occupied_squares, player_occupied_squares):
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

    @staticmethod
    def _get_king_moves(board):
        king_moves = []
        king_attack_offsets = (-9, -8, -7, -1, 1, 7, 8, 9)
        king_position = board.bitboards[constants.KING] & board.bitboards[board.current_player]

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
                if to_square & board.bitboards[board.current_player] != 0:
                    continue
                king_moves.append((from_square, to_square))
            king_position &= king_position - 1
        return king_moves

    @staticmethod
    def get_move_by_figure(board, figure):
        figure_moves = []
        figures = board.bitboards[figure] & board.bitboards[board.current_player]

        while figures:
            from_square = figures & -figures
            if figure == constants.ROOK:
                attacks = ChessEngine._generate_rook_attacks(from_square,
                                                             board.bitboards[
                                                                 constants.WHITE] if board.current_player != constants.WHITE else
                                                             board.bitboards[constants.BLACK], board.bitboards[board.current_player])
            elif figure == constants.BISHOP:
                attacks = ChessEngine._generate_bishop_attacks(from_square,
                                                               board.bitboards[
                                                                   constants.WHITE] if board.current_player != constants.WHITE else
                                                               board.bitboards[constants.BLACK], board.bitboards[board.current_player])
            elif figure == constants.QUEEN:
                attacks = ChessEngine._generate_rook_attacks(from_square,
                                                             board.bitboards[
                                                                 constants.WHITE] if board.current_player != constants.WHITE else
                                                             board.bitboards[constants.BLACK], board.bitboards[board.current_player])
                attacks |= ChessEngine._generate_bishop_attacks(from_square,
                                                                board.bitboards[
                                                                    constants.WHITE] if board.current_player != constants.WHITE else
                                                                board.bitboards[constants.BLACK], board.bitboards[board.current_player])
            elif figure == constants.KING:
                return ChessEngine._get_king_moves(board)
            elif figure == constants.PAWN:
                return ChessEngine.get_pawn_moves(board)
            elif figure == constants.KNIGHT:
                return ChessEngine._get_knight_moves(board)
            else:
                logger.error("Unknown figure: ", figure)

            while attacks:
                to_square = attacks & -attacks
                figure_moves.append((from_square, to_square))
                attacks &= attacks - 1

            figures &= figures - 1

        return figure_moves

    @staticmethod
    def perform_move(move, board, move_type="algebraic", with_validation=True):
        # TODO: Je nach Verwendung der Funktion würde ich hier nicht nochmal alle legalen moves generieren, da der ausgewählte move bereits legal ist --> Laufzeitverlängerung
        if move_type == "algebraic":
            move = ChessEngine.algebraic_move_to_binary(move)
        if with_validation:
            legal_moves = ChessEngine.filter_illegal_moves(board, ChessEngine.generate_moves(board))
            if move not in legal_moves and move_type != "algebraic":
                raise IllegalMoveException(ChessEngine.binary_move_to_algebraic(move[0], move[1]))
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

    @staticmethod
    def is_in_check(board, isOpponent=False):
        # move is a tuple containing start and destination bitboards, checks if input player is in check
        # TODO: king - king face off not included yet
        player = board.current_player if not isOpponent else board.get_opponent(board.current_player)
        boardOpponent = copy.deepcopy(board)
        boardOpponent.current_player = board.get_opponent(player)
        legal_moves_opponent = ChessEngine.generate_moves(boardOpponent)
        dest_legal_moves = [elem[1] for elem in legal_moves_opponent]
        in_check = [dest & (board.bitboards[constants.KING] & board.bitboards[player]) for dest in
                    dest_legal_moves]
        return any(elem != 0 for elem in in_check)

    @staticmethod
    def is_check_mate(board):
        if not ChessEngine.is_in_check(board):
            return False
        legal_moves = ChessEngine.generate_moves(board)
        for move in legal_moves:
            board_after_move = copy.deepcopy(board)
            ChessEngine.perform_move(move, board_after_move, move_type="binary", with_validation=False)
            if not ChessEngine.is_in_check(board_after_move, isOpponent=True):
                board.game_result = board.get_opponent(board.current_player)
                return False
        return True

    @staticmethod
    def is_draw(legal_moves, board):
        # TODO: There is one more draw rule "50-Züge-Regel"
        if not legal_moves and not board.is_in_check(board):
            print("Draw by Patt!")
            board.game_result = constants.WHITE if board.current_player == constants.BLACK else constants.BLACK
            return True
        if ChessEngine._is_repetition_draw(board.board_history):
            print("Draw by repetition!")
            board.game_result = constants.WHITE if board.current_player == constants.BLACK else constants.BLACK
            return True
        return False

    @staticmethod
    def _is_repetition_draw(board_list):
        # Wenn in einer Schachpartie dreimal die exakt gleiche Stellung auf dem Brett auftritt, endet die Partie in einem Remis. 
        # Mit exakt ist gemeint, dass jeweils der gleiche Spieler am Zug sein muss. Optionen wie das Rochaderecht oder En passant müssen ebenfalls identisch sein.
        # TODO: include rochade, ...
        for sublist in board_list:
            # print(board_list.count(sublist))
            if board_list.count(sublist) > 2:
                return True
        return False

    @staticmethod
    def algebraic_move_to_binary(move):
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

        return from_square, to_square

    @staticmethod
    def is_move_legal(move, board):
        board_after_move = copy.deepcopy(board)
        ChessEngine.perform_move(move, board_after_move, move_type="binary", with_validation=False)
        is_in_check = ChessEngine.is_in_check(board_after_move, isOpponent=True)
        return not is_in_check

    @staticmethod
    def filter_illegal_moves(board, moves):
        legal_moves = [
            move for move in moves if ChessEngine.is_move_legal(move, board)
        ]

        return legal_moves

    @staticmethod
    def generate_moves(board):
        moves = []
        moves += ChessEngine.get_move_by_figure(board, constants.PAWN)
        moves += ChessEngine.get_move_by_figure(board, constants.KNIGHT)
        moves += ChessEngine.get_move_by_figure(board, constants.BISHOP)
        moves += ChessEngine.get_move_by_figure(board, constants.ROOK)
        moves += ChessEngine.get_move_by_figure(board, constants.QUEEN)
        moves += ChessEngine.get_move_by_figure(board, constants.KING)

        return moves

    @staticmethod
    def print_legal_moves(board):
        legal_moves = ChessEngine.generate_moves(board)
        print(
            "\nLegal moves for the current player ({}):".format(
                "constants.WHITE" if board.current_player == constants.WHITE else "constants.BLACK"
            )
        )
        for move in legal_moves:
            from_square, to_square = move
            print(ChessEngine.binary_move_to_algebraic(from_square, to_square))

    @staticmethod
    def binary_move_to_algebraic(from_square, to_square):
        def binary_field_to_algebraic(field):
            col_names = "abcdefgh"
            row_names = "12345678"

            col = col_names[(field.bit_length() - 1) % 8]
            row = row_names[(field.bit_length() - 1) // 8]

            return f"{col}{row}"

        from_field = binary_field_to_algebraic(from_square)
        to_field = binary_field_to_algebraic(to_square)

        return f"{from_field}{to_field}"
