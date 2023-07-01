from ChessEngine import ChessEngine
from ChessPrintService import ChessPrintService
import constants
import copy
import math
from loguru import logger
import time
import numpy as np

HASH_BOARD = np.random.randint(0, pow(2, 64), size=(64,12), dtype='uint64')
RANDOM_INT_WHITE = int(np.random.randint(0, pow(2, 64), dtype='uint64'))
RANDOM_INT_BLACK = int(np.random.randint(0, pow(2, 64), dtype='uint64'))
hash_table = {}

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
        self.game_phase = "midgame"
        board_after_move = copy.deepcopy(self)
        if move:
            ChessEngine.perform_move(move, board_after_move, move_type, with_validation=False)
            
        CENTER__MASK = int("0b0000000000000000001111000011110000111100001111000000000000000000", 2)
        CENTER_CONTROL_VALUE = 100
        score = 0
        opponent = ChessBoard.get_opponent(self.current_player) # this is correct, since we always want to evaluate the board for the current player, before or after his move

        
        occupied_squares = board_after_move.bitboards[constants.WHITE] | board_after_move.bitboards[constants.BLACK]
        
        piece_values = constants.PIECE_VALUES_MIDGAME if self.game_phase == "midgame" or self.game_phase == "opening" else constants.PIECE_VALUES_ENDGAME

        while occupied_squares:
            square = occupied_squares & -occupied_squares
            piece = board_after_move._get_piece_at_square(square)
            occupied_squares &= occupied_squares - 1
            
            # Sum up all the static values of all figures on the board
            piece_value = piece_values[piece]
            score += piece_value if square & board_after_move.bitboards[self.current_player] else -piece_value
            
            # Bonus based on the pawn structure: isolated, passed and connected
            if piece == constants.PAWN:
                board_after_move._get_pawn_value(square)
                
            # Bonus points for controlling the center
            if square & CENTER__MASK:
                row, col = board_after_move._get_row_col_from_square(square)
                center_distance = abs(row - 3.5) + abs(col - 3.5)
                score += CENTER_CONTROL_VALUE / (center_distance + 1) if square & board_after_move.bitboards[self.current_player] else - CENTER_CONTROL_VALUE / (center_distance + 1)
            
            # Bonus based on the position of the figure: Piece square tables for opening, midgame and endgame
            if square & board_after_move.bitboards[self.current_player]:
                score += constants.get_figure_value(self.current_player, square.bit_length() - 1, piece, self.game_phase)
            elif square & board_after_move.bitboards[opponent]:
                score -= constants.get_figure_value(opponent, square.bit_length() - 1, piece, self.game_phase)
                
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
            score -= 200  # Penalty for own king in check
        else:
            score += 100  # Bonus for king's safety
        if ChessEngine.is_game_over(self):
            score -= 100000
        if ChessEngine.is_game_won(self):
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
    
    def _get_pawn_value(self, pawn_position):
        """
        Define the pawn value based on its positioning to other figures: isolated, connected, passed
        See: https://en.wikipedia.org/wiki/Chess_piece_relative_value
        """
        
        bitboard = self.bitboards[constants.PAWN] & self.bitboards[self.current_player]
        opponent_pawns = self.bitboards[constants.PAWN] & self.bitboards[self.get_opponent(self.current_player)]

        if self.game_phase == "midgame" or self.game_phase == "opening":
            pawn_value = constants.PIECE_VALUES_MIDGAME[constants.PAWN]
        elif self.game_phase == "endgame":
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
    
    def set_game_phase(self, move_actually_executed):
        # 1. Piece developement: Opening -> midgame
        if self.game_phase == "opening" and self.opening_count >= 7:
            self.game_phase = "midgame"
            # if move_actually_executed:
            #     logger.debug("Switched to game phase midgame!")
            
        # 2. Piece count: midgame -> endgame: In general, the midgame is characterized by a higher number of pieces on the board, while the endgame typically has fewer pieces remaining
        if self.game_phase == "midgame":
            piece_count_limit = 16 # at 8 remaining pieces, we enter the endgame
            all_pieces = self.bitboards[constants.WHITE] | self.bitboards[constants.BLACK]
            count_pieces = ChessBoard._count_set_bits(all_pieces)
            if count_pieces <= piece_count_limit:
                self.game_phase = "endgame"
                # logger.debug("Switched to game phase endgame!")
            
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


    def zobrist_board_hash(self):
        hash = RANDOM_INT_WHITE if self.current_player == constants.WHITE else RANDOM_INT_BLACK
        occupied_fields = self.bitboards[constants.WHITE] | self.bitboards[constants.BLACK]
        while occupied_fields:
            figure_square = occupied_fields & -occupied_fields
            occupied_fields &= occupied_fields - 1
            figure = self._get_piece_at_square(figure_square)
            cell = figure_square.bit_length() - 1
            # HASH_BOARD assignes each cell and each figure a random value, by xor with each piece we get a unique hash for each board state
            num = HASH_BOARD[cell][figure - 2 if figure_square & self.bitboards[constants.WHITE] else figure + 4]
            hash ^= int(num)
        return hash

    def iterative_depth_search(self, max_depth = 4, time_limit = 15, with_cut_off=True, with_time_limit = True, with_max_depth = False):
        """
        This method iterates through the levels of the search tree, 
        which is way faster in combination with move ordering and transposition tables.
        
        We always take the result from the deepest depth.
        
        The self.current_player is always the maximizing player. Therefore, larger scores are better.
        """
        best_move = None
        counter = 0
        start_time = time.time()
        global hash_table
        hash_table = {}
        if with_time_limit and not with_max_depth:
            max_depth = 10000 # take an insane large value, since we have a time limit
        
        for depth in range(1, max_depth + 1):
            score, counter, _,  move, is_time_over = self.alpha_beta_max(-math.inf, math.inf, depth, 0, counter, time_limit, start_time, with_time_limit, with_cut_off)
            if not is_time_over:
                best_move = move
                # logger.debug("Vorläufig bester Zug: {}, Tiefe: {}, Score: {}".format(ChessEngine.binary_move_to_algebraic(move[0], move[1]), depth, score))
            else:
                break

        return best_move, counter

    def store_hash_board_state(self, depth, score, type, move):
        hash_key = self.zobrist_board_hash()
        hash_table[hash_key] = {
            'depth': depth,
            'flag': type, # type is either exact, upperbound or lowerbound
            'value': score, 
            'move': move
        }

    def alpha_beta_max(self, alpha, beta, depth_left, depth,  counter, time_limit, start_time, with_time_limit, with_cut_off=True):
        # time_management: 
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit and with_time_limit:
            return None, counter + 1, None, None, True
        # transposition table:
        hash_key = self.zobrist_board_hash()
        if hash_key in hash_table:
            entry = hash_table[hash_key]
            # the stored depth has to be larger than the current depth to be meaningful
            if entry['depth'] >= depth:
                if entry['flag'] == 'exact':
                    return entry['value'], counter + 1, entry['flag'], entry['move'], False
                elif entry['flag'] == 'lowerbound':
                    alpha = max(alpha, entry['value'])

                if alpha >= beta:
                    return entry['value'], counter + 1, entry['flag'], entry['move'], False

        # alpha beta:
        if depth_left == 0:
            return self.evaluate_board(), counter + 1, "lowerbound", None, False
        elif ChessEngine.is_game_over(self):
            return self.evaluate_board(), counter + 1, "exact", None, False
        moves = ChessEngine.generate_moves(self)
        legal_moves = ChessEngine.filter_illegal_moves(self, moves)
        legal_moves = sorted(legal_moves, key=lambda move: ChessEngine.get_move_value(self, move), reverse=True)
        best_move = None
        for move in legal_moves:
            
            board_after_move = copy.deepcopy(self)
            ChessEngine.perform_move(move, board_after_move, move_type="binary", with_validation=False)
            if ChessEngine.is_draw(legal_moves, board_after_move):
                score = -board_after_move.evaluate_board() # negative because we evaluate the board for the oppponent already
                flag = "exact"
            else:
                score, counter, flag, _, is_time_over  = board_after_move.alpha_beta_min(alpha, beta, depth_left - 1, depth + 1, counter, time_limit, start_time, with_time_limit, with_cut_off)
                if is_time_over: # time_management
                    return None, counter + 1, None, None, True
                board_after_move.store_hash_board_state(depth + 1, score, type=flag, move= move)
            if score >= beta and with_cut_off == True:
                return beta, counter+1, "lowerbound", best_move, False
            if score > alpha:
                best_move = move
                alpha = score
        return alpha, counter+1, flag, best_move, False

    def alpha_beta_min(self, alpha, beta, depth_left, depth, counter, time_limit, start_time, with_time_limit, with_cut_off=True):
        # time_management: 
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit and with_time_limit:
            return None, counter + 1, None, None, True
        
        # transposition table:
        hash_key = self.zobrist_board_hash()
        if hash_key in hash_table:
            entry = hash_table[hash_key]
            # the stored depth has to be larger than the current depth to be meaningful
            if entry['depth'] >= depth:
                if entry['flag'] == 'exact':
                    return entry['value'], counter + 1, entry['flag'], entry['move'], False
                elif entry['flag'] == 'upperbound':
                    beta = min(beta, entry['value'])

                if alpha >= beta:
                    return entry['value'], counter + 1, entry['flag'], entry['move'], False

        # alpha beta:
        if depth_left == 0:
            return -self.evaluate_board(), counter + 1, "upperbound", None, False
        elif ChessEngine.is_game_over(self):
            return -self.evaluate_board(), counter + 1, "exact", None, False
        moves = ChessEngine.generate_moves(self)
        legal_moves = ChessEngine.filter_illegal_moves(self, moves)
        legal_moves = sorted(legal_moves, key=lambda move: ChessEngine.get_move_value(self, move), reverse=True)
        best_move = None
        for move in legal_moves:
            board_after_move = copy.deepcopy(self)
            ChessEngine.perform_move(move, board_after_move, move_type="binary", with_validation=False)
            if ChessEngine.is_draw(legal_moves, board_after_move):
                score = board_after_move.evaluate_board() # negative because we evaluate the board for the oppponent already
                flag = "exact"
            else:
                score, counter, flag,  _, is_time_over = board_after_move.alpha_beta_max(alpha, beta, depth_left - 1, depth + 1, counter, time_limit, start_time, with_time_limit, with_cut_off)
                if is_time_over: # time_management
                    return None, counter + 1, None, None, True
                board_after_move.store_hash_board_state(depth + 1, score, type=flag, move= move)
                
            if score <= alpha and with_cut_off == True:
                return alpha, counter+1, "upperbound", best_move, False
            if score < beta:
                best_move = move
                beta = score
        return beta, counter+1, flag, best_move, False

    @staticmethod
    def get_opponent(player):
        return constants.WHITE if player == constants.BLACK else constants.BLACK


if __name__ == "__main__":
    # board = ChessBoard()
    # board.load_from_fen("rn2k3/pp4p1/4p2p/2P1N3/3P1B2/2N5/1P4PP/R4K1R w KQq - 0 1")
    service = ChessPrintService()
    pawn = int("0b0000000000000000000000000000000000000000000000000000000000010000", 2)
    # pawn=int("0b0000000000000000000000000000000000010000000000001111111111111111", 2)
    #      int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
    # figure_square = 73786976294838206464
    # figure = 2
    # cell = 66
    # occupied_fields = 0
    # white = 73786976364229083809
    # black = 1387971252102103040
    
    # binary_number = bin(figure_square)[2:]
    # binary_number_with_newlines = '\n'.join(binary_number[i:i+8] for i in range(0, len(binary_number), 8))
    # print(binary_number_with_newlines)    
    # print(figure_square.bit_length() - 1)

    # service.print_binary_bitboard(black)
    # board.evaluate_board()
    
    board = ChessBoard()
    board.load_from_fen("rnbqkb1r/1p1p1ppp/p3pn2/2p5/4P3/PPNP4/2P2PPP/R1BQKBNR b KQkq - 0 1")
    best_move, counter = board.iterative_depth_search(max_depth = 4, time_limit = 15, with_cut_off=True, with_time_limit = True, with_max_depth = False)
    # ChessEngine.perform_move(best_move, board, move_type="binary")
    # # service.print_binary_bitboard(board.bitboards[constants.WHITE])
    # # service.print_binary_bitboard(board.bitboards[constants.BLACK])

    # print(ChessEngine.binary_move_to_algebraic(best_move[0], best_move[1]))
    
    # best_move, counter = board.iterative_depth_search(3, True)
    # print(ChessEngine.binary_move_to_algebraic(best_move[0], best_move[1]))
    # ChessEngine.perform_move(best_move, board, move_type="binary")
    
    # best_move, counter = board.iterative_depth_search(3, True)
    # print(ChessEngine.binary_move_to_algebraic(best_move[0], best_move[1]))
    # ChessEngine.perform_move(best_move, board, move_type="binary")

    
    # best_move, counter = board.iterative_depth_search(3, True)
    # print(best_move)
    # moves = ChessEngine.get_move_by_figure(board, constants.KING)
    # legal_moves = ChessEngine.filter_illegal_moves(board, moves)
    # print(legal_moves)
    # print(ChessEngine.is_check_mate(board))
