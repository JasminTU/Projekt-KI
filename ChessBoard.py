from ChessEngine import ChessEngine
from ChessPrintService import ChessPrintService
import constants
import copy
import math
from loguru import logger
import time


class ChessBoard:
    def __init__(self):
        self.bitboards = None
        self.initialize_bitboards()
        self.current_player = constants.WHITE
        self.chessEngine = ChessEngine()
        self.game_result = None
        self.board_history = []
        self.pawn_not_moved_counter = 0
        self.opening_bitboard = int("0b1111111110111100000000000000000000000000000000000011111011111111", 2)
        self.opening_count = 0
        self.game_phase = "opening"

    def initialize_bitboards(self):
        self.bitboards = [0] * 8

        # Set initial positions for constants.WHITE, black and all pieces using binary literals
        self.bitboards[constants.WHITE] = int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
        self.bitboards[constants.BLACK] = int("0b1111111111111111000000000000000000000000000000000000000000000000", 2)
        self.bitboards[constants.PAWN] = int("0b0000000011111111000000000000000000000000000000001111111100000000", 2)
        self.bitboards[constants.KNIGHT] = int("0b0100001000000000000000000000000000000000000000000000000001000010", 2)
        self.bitboards[constants.BISHOP] = int("0b0010010000000000000000000000000000000000000000000000000000100100", 2)
        self.bitboards[constants.ROOK] = int("0b1000000100000000000000000000000000000000000000000000000010000001", 2)
        self.bitboards[constants.QUEEN] = int("0b0000100000000000000000000000000000000000000000000000000000001000", 2)
        self.bitboards[constants.KING] = int("0b0001000000000000000000000000000000000000000000000000000000010000", 2)

    def load_from_fen(self, fen):
        fen_parts = fen.split(" ")
        piece_positions = fen_parts[0]
        current_player_fen = fen_parts[1]

        self.current_player = constants.WHITE if current_player_fen == "w" else constants.BLACK

        rows = piece_positions.split("/")

        self.bitboards = [0] * 8

        piece_symbols = {
            "P": constants.PAWN,
            "N": constants.KNIGHT,
            "B": constants.BISHOP,
            "R": constants.ROOK,
            "Q": constants.QUEEN,
            "K": constants.KING,
        }

        # Process rows in reverse order
        for row_index, row in enumerate(reversed(rows)):
            col_index = 0
            for char in row:
                if char.isdigit():
                    col_index += int(char)
                else:
                    color = constants.WHITE if char.isupper() else constants.BLACK
                    piece_type = piece_symbols[char.upper()]

                    square = 1 << (row_index * 8 + col_index)

                    self.bitboards[color] |= square
                    self.bitboards[piece_type] |= square

                    col_index += 1
        # PrintBitBoardService.print_bitboards(self.bitboards)
        # PrintBitBoardService.print_board(self.bitboards)

    def evaluate_board(self, move=None, move_type="algebraic"):
        # Evaluate the board after a move or on current board
        # The evaluation method should be symmetric
        # TODO: there are a lot of hardcoded values to compute the score, need for improvement
        game_phase = "midgame"
        board_after_move = copy.deepcopy(self)
        if move:
            ChessEngine.perform_move(move, board_after_move, move_type, with_validation=False)
            
        CENTER__MASK = int("0b0000000000000000001111000011110000111100001111000000000000000000", 2)
        CENTER_CONTROL_VALUE = 100
        score = 0
        opponent = ChessBoard.get_opponent(self.current_player) # this is correct, since we always want to evaluate the board for the current player, before or after his move

        
        occupied_squares = board_after_move.bitboards[constants.WHITE] | board_after_move.bitboards[constants.BLACK]
        piece_values = constants.PIECE_VALUES_MIDGAME if game_phase == "midgame" or game_phase == "opening" else constants.PIECE_VALUES_ENDGAME

        while occupied_squares:
            square = occupied_squares & -occupied_squares
            piece = board_after_move._get_piece_at_square(square)
            occupied_squares &= occupied_squares - 1
            
            # Sum up all the static values of all figures on the board
            piece_value = piece_values[piece]
            score += piece_value if square & board_after_move.bitboards[self.current_player] else -piece_value
            
            # Bonus based on the pawn structure: isolated, passed and connected
            if piece == constants.PAWN:
                board_after_move._get_pawn_value(square, game_phase)
                
            # Bonus points for controlling the center
            if square & CENTER__MASK:
                row, col = board_after_move._get_row_col_from_square(square)
                center_distance = abs(row - 3.5) + abs(col - 3.5)
                score += CENTER_CONTROL_VALUE / (center_distance + 1) if square & board_after_move.bitboards[self.current_player] else - CENTER_CONTROL_VALUE / (center_distance + 1)
            
            # Bonus based on the position of the figure: Piece square tables for mid and endgame
            if square & board_after_move.bitboards[self.current_player]:
                score += constants.get_figure_value(self.current_player, square.bit_length() - 1, piece, game_phase)
            elif square & board_after_move.bitboards[opponent]:
                score -= constants.get_figure_value(opponent, square.bit_length() - 1, piece, game_phase)
                
            # Penalty for pieces near the enemy king
            if square & board_after_move.bitboards[self.current_player]:
                enemy_king_pos = board_after_move.bitboards[opponent] & board_after_move.bitboards[constants.KING]
                distance_to_enemy_king = board_after_move._square_distance(square, enemy_king_pos)
                score -= 0.2 / (distance_to_enemy_king + 1)
            # Bonus for enemy pieces near the current players king
            if square & board_after_move.bitboards[opponent]:
                king_pos = board_after_move.bitboards[self.current_player] & board_after_move.bitboards[constants.KING]
                distance_to_own_king = board_after_move._square_distance(square, king_pos)
                score += 0.2 / (distance_to_own_king + 1)

        # Evaluate king's safety
        if ChessEngine.is_in_check(self):
            score -= 100  # Penalty for own king in check
        else:
            score += 100  # Bonus for king's safety
        if ChessEngine.is_check_mate(self) or ChessEngine.opponent_is_king_on_the_hill(self):
            score -= 100000  # Penalty for own king in check mate
        if ChessEngine.opponent_is_check_mate(self):
            score += 100000
            
        # Bonus for king's position near the center
        king_position = self.bitboards[self.current_player] & self.bitboards[constants.KING]
        row, col = self._get_row_col_from_square(king_position)
        center_distance = abs(row - 3.5) + abs(col - 3.5)
        score += CENTER_CONTROL_VALUE / (center_distance + 1)
        # Penalty for opponent king's position near the center
        opp_king_position = self.bitboards[opponent] & self.bitboards[constants.KING]
        row, col = self._get_row_col_from_square(opp_king_position)
        center_distance = abs(row - 3.5) + abs(col - 3.5)
        score -= CENTER_CONTROL_VALUE / (center_distance + 1)
        
        return score
    
    def _get_pawn_value(self, pawn_position, game_phase):
        """
        Define the pawn value based on its positioning to other figures: isolated, connected, passed
        See: https://en.wikipedia.org/wiki/Chess_piece_relative_value
        """
        
        bitboard = self.bitboards[constants.PAWN] & self.bitboards[self.current_player]
        opponent_pawns = self.bitboards[constants.PAWN] & self.bitboards[self.get_opponent(self.current_player)]

        if game_phase == "midgame":
            pawn_value = constants.PIECE_VALUES_MIDGAME[constants.PAWN]
        elif game_phase == "endgame":
            pawn_value = constants.PIECE_VALUES_ENDGAME[constants.PAWN]
        else:
            logger.error("Error in _get_pawn_value(): No such game phase.")
        
        # bonuses are in %
        isolated_bonus = -10
        connected_bonus = 15
        passed_bonus = 35
        passed_and_connected_bonus = 100
            
        if ChessBoard._is_pawn_isolated(bitboard, pawn_position) == 0:
            pawn_value *= ((isolated_bonus + 100)/100)
        elif ChessBoard._is_pawn_connected(bitboard, pawn_position) != 0 and self._is_pawn_passed(opponent_pawns, pawn_position) == 0:
            pawn_value *= ((passed_and_connected_bonus + 100)/100)
        elif ChessBoard._is_pawn_connected(bitboard, pawn_position) != 0:
            pawn_value *= ((connected_bonus + 100)/100)
        elif self._is_pawn_passed(opponent_pawns, pawn_position) == 0:
            pawn_value *= ((passed_bonus + 100)/100)
        return pawn_value
    
    def set_game_phase(self):
        # 1. Piece developement: Opening -> midgame
        if self.game_phase == "opening" and self.opening_count >= 7:
            self.game_phase = "midgame"
            
        # 2. Piece count: midgame -> endgame: In general, the midgame is characterized by a higher number of pieces on the board, while the endgame typically has fewer pieces remaining
        if self.game_phase == "midgame":
            piece_count_limit = 8 # at 8 remaining pieces, we enter the endgame
            all_pieces = self.bitboards[constants.WHITE] | self.bitboards[constants.BLACK]
            count_pieces = ChessBoard._count_set_bits(all_pieces)
            if count_pieces <= piece_count_limit:
                self.game_phase = "endgame"
            
    def get_game_phase(self):
        return self.game_phase
        
    @staticmethod
    def _count_set_bits(bitboard):
        count = 0
        while bitboard:
            bitboard &= bitboard - 1
            count += 1
        return count
   
    @staticmethod
    def _is_pawn_isolated(bitbaord, pawn_position):
        pawn_mask = (pawn_position & constants.NOT_LEFT_EDGE) >> 1 | (pawn_position & constants.NOT_RIGHT_EDGE) << 1 | \
                    (pawn_position & constants.NOT_RIGHT_EDGE) << 9 | (pawn_position & constants.NOT_LEFT_EDGE) << 7 | (pawn_position & constants.NOT_LEFT_EDGE) >> 9 | (pawn_position & constants.NOT_RIGHT_EDGE) >> 7
        return pawn_mask & bitbaord
    
    @staticmethod
    def _is_pawn_connected(bitbaord, pawn_position):
        pawn_mask = (pawn_position & constants.NOT_RIGHT_EDGE) << 9 | (pawn_position & constants.NOT_LEFT_EDGE) << 7 | (pawn_position & constants.NOT_LEFT_EDGE) >> 9 | (pawn_position & constants.NOT_RIGHT_EDGE) >> 7
        return pawn_mask & bitbaord
    
    def _is_pawn_passed(self, opponent_pawns, pawn_position):
        row = (pawn_position.bit_length()-1) // 8
        pawn_mask = 0
        while 0 < row < 7:
            position = (pawn_position & constants.NOT_TOP_EDGE) << 8 | (pawn_position & constants.NOT_LEFT_EDGE) << 7 | (pawn_position & constants.NOT_RIGHT_EDGE) << 9 if self.current_player == constants.WHITE else (pawn_position & constants.NOT_BOTTOM_EDGE) >> 8 | (pawn_position & constants.NOT_RIGHT_EDGE) >> 7 | (pawn_position & constants.NOT_LEFT_EDGE) >> 9
            pawn_position = pawn_position << 8 if self.current_player == constants.WHITE else pawn_position >> 8
            row = row +1 if self.current_player == constants.WHITE else row - 1
            pawn_mask |= position
        return pawn_mask & opponent_pawns
    
    def _square_distance(self, square1, square2):
        # Assuming square1 and square2 are bitboards with a single bit set to 1
        row1, col1 = self._get_row_col_from_square(square1)
        row2, col2 = self._get_row_col_from_square(square2)
        distance = max(abs(row1 - row2), abs(col1 - col2))
        return distance
    
    def _get_row_col_from_square(self, square):
        # Assuming square is a bitboard with a single bit set to 1
        index = square.bit_length() - 1  # Get the index of the set bit

        row, col = divmod(index, 8)  # Divide index by 8 to get row and column

        return row, col

    
    def _get_piece_at_square(self, square):
        if self.bitboards[constants.PAWN] & square:
            return constants.PAWN
        if self.bitboards[constants.KNIGHT] & square:
            return constants.KNIGHT
        if self.bitboards[constants.BISHOP] & square:
            return constants.BISHOP
        if self.bitboards[constants.ROOK] & square:
            return constants.ROOK
        if self.bitboards[constants.QUEEN] & square:
            return constants.QUEEN
        if self.bitboards[constants.KING] & square:
            return constants.KING
        service = ChessPrintService()
        logger.error("Error in method _get_piece_at_square(). No figure is on the input square: {}. \n Given the board: {}", ChessEngine.binary_field_to_algebraic(square), service.print_board(self.bitboards))

    def iterative_depth_search(self, max_depth, time_limit = 12000, with_cut_off=True):
        best_score = None
        best_move = None
        counter = 0
        start_time = time.time()
        
        for depth in range(1, max_depth + 1):
            score, counter, move = self.alpha_beta_max(-math.inf, math.inf, depth, counter, with_cut_off)
            if best_score is None or score > best_score:
                best_score = score
                best_move = move
                
            # elapsed_time = time.time() - start_time
            # if elapsed_time >= time_limit:
            #     break
        return best_move, counter

    def alpha_beta_max(self, alpha, beta, depth_left, counter, with_cut_off=True):
        if depth_left == 0 or ChessEngine.is_game_over(self):
            return self.evaluate_board(), counter + 1, None
        moves = ChessEngine.generate_moves(self)
        legal_moves = ChessEngine.filter_illegal_moves(self, moves)
        best_move = None
        for move in legal_moves:
            board_after_move = copy.deepcopy(self)
            ChessEngine.perform_move(move, board_after_move, move_type="binary", with_validation=False)
            if ChessEngine.is_draw(legal_moves, board_after_move):
                score = -board_after_move.evaluate_board()
            else:
                score, counter, _ = board_after_move.alpha_beta_min(alpha, beta, depth_left - 1, counter, with_cut_off)
            
            if score >= beta and with_cut_off:
                return beta, counter+1, None
            if score > alpha:
                best_move = move
                alpha = score
        return alpha, counter+1, best_move

    def alpha_beta_min(self, alpha, beta, depth_left, counter, with_cut_off=True):
        if depth_left == 0 or ChessEngine.is_game_over(self):
            return -self.evaluate_board(), counter + 1, None
        moves = ChessEngine.generate_moves(self)
        legal_moves = ChessEngine.filter_illegal_moves(self, moves)
        best_move = None
        for move in legal_moves:
            board_after_move = copy.deepcopy(self)
            ChessEngine.perform_move(move, board_after_move, move_type="binary", with_validation=False)
            if ChessEngine.is_draw(legal_moves, board_after_move):
                score = -board_after_move.evaluate_board()
            else:
                score, counter, _ = board_after_move.alpha_beta_max(alpha, beta, depth_left - 1, counter, with_cut_off)
            if score <= alpha and with_cut_off:
                return alpha, counter+1, None
            if score < beta:
                best_move = move
                beta = score
        return beta, counter+1, best_move

    @staticmethod
    def get_opponent(player):
        return constants.WHITE if player == constants.BLACK else constants.BLACK


if __name__ == "__main__":
    board = ChessBoard()
    board.load_from_fen("rnbqkbnr/pppppppp/8/8/8/3Q4/PPPPPPPP/RNB1KBNR w KQkq - 0 1")
    service = ChessPrintService()
    pawn = int("0b0000000000000000000000000000000000000000000000000000000000010000", 2)
    # pawn=int("0b0000000000000000000000000000000000010000000000001111111111111111", 2)
    #      int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
    service.print_binary_bitboard(pawn)
    board.evaluate_board()
