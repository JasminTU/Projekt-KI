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
        board_after_move = copy.deepcopy(self)
        if move:
            ChessEngine.perform_move(move, board_after_move, move_type, with_validation=False)
            
        CENTER__MASK = int("0b0000000000000000001111000011110000111100001111000000000000000000", 2)
        score = 0
        opponent = ChessBoard.get_opponent(self.current_player) # this is correct, since we always want to evaluate the board for the current player, before or after his move
        piece_values = {
            constants.PAWN: 1, constants.KNIGHT: 3, constants.BISHOP: 3, constants.ROOK: 5, constants.QUEEN: 9, constants.KING: 20
        }
        occupied_squares = board_after_move.bitboards[constants.WHITE] | board_after_move.bitboards[constants.BLACK]

        while occupied_squares:
            square = occupied_squares & -occupied_squares
            piece = board_after_move._get_piece_at_square(square)
            occupied_squares &= occupied_squares - 1
            piece_value = piece_values[piece]
            score += piece_value if square & board_after_move.bitboards[self.current_player] else -piece_value
            # Add bonus points for controlling the center
            if square & CENTER__MASK:
                row, col = board_after_move._get_row_col_from_square(square)
                center_distance = abs(row - 3.5) + abs(col - 3.5)
                score += 0.5 / (center_distance + 1) if square & board_after_move.bitboards[self.current_player] else - 0.5 / (center_distance + 1)
            
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
            score -= 1  # Penalty for own king in check
        else:
            score += 1  # Bonus for king's safety
        if ChessEngine.is_check_mate(self) or ChessEngine.opponent_is_king_on_the_hill(self):
            score -= 100  # Penalty for own king in check mate
        if ChessEngine.opponent_is_check_mate(self):
            score += 100
            
        # Bonus for king's position near the center
        king_position = self.bitboards[self.current_player] & self.bitboards[constants.KING]
        row, col = self._get_row_col_from_square(king_position)
        center_distance = abs(row - 3.5) + abs(col - 3.5)
        score += 10 / (center_distance + 1)
        # Penalty for opponent king's position near the center
        opp_king_position = self.bitboards[opponent] & self.bitboards[constants.KING]
        row, col = self._get_row_col_from_square(opp_king_position)
        center_distance = abs(row - 3.5) + abs(col - 3.5)
        score -= 10 / (center_distance + 1)
        
        # TODO: evaluate pawn position and pawn type; calculate a (negative?) score for draw;
        
        return score
    
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
        legal_moves = sorted(legal_moves, key=lambda move: ChessEngine.get_move_value(self, move), reverse=True)
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
        legal_moves = sorted(legal_moves, key=lambda move: ChessEngine.get_move_value(self, move), reverse=True)
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

