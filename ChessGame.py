from ChessPrintService import ChessPrintService
from ChessBoard import ChessBoard
from ChessEngine import ChessEngine
import constants
import re
from loguru import logger
import sys
from stockfish_ai import KingOfTheHillAI

class ChessGame:
    def __init__(self, board, max_depth, time_limit, isBlackAI=True, isWhiteAI=True, isBlackStockfishAI = False, isWhiteStockfishAI = False):
        self.board = board
        self.move_number = 1
        self.isBlackAI = isBlackAI
        self.isBlackStockfishAI = isBlackStockfishAI
        self.isWhiteStockfishAI = isWhiteStockfishAI
        self.isWhiteAI = isWhiteAI
        self.currentLegalMoves = []
        self.time_limit = time_limit
        self.max_depth = max_depth
        self.stockfish_ai = KingOfTheHillAI()

    def play(self):
        while True:
            if self.process_next_move() == "checkmate" or self.process_next_move() == "draw":
                break

    def process_next_move(self, print_board=True, with_cut_off=True, with_time_limit = True):
        if print_board:
            self.print_board()
        self.currentLegalMoves = self.get_legal_moves()
        # Check for draw and checkmate before the move is exercised
        if ChessEngine.is_draw(self.currentLegalMoves, self.board):  # more detailed print is in draw function
            return "draw"
        if ChessEngine.is_game_over(self.board) or ChessEngine.is_game_won(self.board):    
            winner = "White" if self.board.game_result == constants.WHITE else "Black"
            print("Checkmate! Winner is ", winner)
            return "checkmate"

        if self.is_ai_turn():
            move, counter = self.get_ai_move(print_board, with_cut_off, with_time_limit)
        elif self.is_stockfish_ai_turn():
            move = ChessEngine.algebraic_move_to_binary(self.get_stockfish_move())
            counter = -1
        else:
            move = ChessEngine.algebraic_move_to_binary(self.get_human_move())
            counter = -1

        self.perform_move(move)
        self.board.previous_moves.append(ChessEngine.binary_move_to_algebraic(move[0], move[1]))
        return move, counter


    def print_board(self):
        ChessPrintService.print_board(self.board.bitboards)

    def is_ai_turn(self):
        return (self.isWhiteAI and self.move_number % 2 == constants.BLACK) or (
                self.isBlackAI and self.move_number % 2 == constants.WHITE)
    
    def is_stockfish_ai_turn(self):
        return (self.isWhiteStockfishAI and self.move_number % 2 == constants.BLACK) or (
                self.isBlackStockfishAI and self.move_number % 2 == constants.WHITE)

    def get_human_move(self):
        str = "White" if self.board.current_player == constants.WHITE else "Black"
        user_input = input(f"Move {self.move_number} by { str}: ")
        while not self.validate_input(user_input):
            print("Invalid input. Enter a move of the form a1a2 (start square->destination square).")
            user_input = input(f"Move {self.move_number} by {str}: ")
        return user_input

    def validate_input(self, user_input):
        pattern = r'^[a-h][1-8][a-h][1-8]$'
        return re.match(pattern, user_input) is not None

    def get_stockfish_move(self, print_move = True):
        best_move = self.stockfish_ai.get_best_move(self.board, self.time_limit)
        if print_move:
            str = "White" if self.board.current_player == constants.WHITE else "Black"
            print(f"Move {self.move_number} by {str} (AI): {best_move}")
        return best_move

    def get_ai_move(self, print_move=True, with_cut_off=True, with_time_limit = True):

        if len(self.currentLegalMoves) == 0:
            logger.error("List is empty. This case should be captured as a check mate or draw!")
            sys.exit(1)
        best_move, counter = self.board.iterative_depth_search(max_depth=self.max_depth, time_limit = self.time_limit, with_cut_off= with_cut_off, with_time_limit = with_time_limit)
        if print_move:
            str = "White" if self.board.current_player == constants.WHITE else "Black"
            print(f"Move {self.move_number} by {str} (AI): {ChessEngine.binary_move_to_algebraic(best_move[0], best_move[1])}")
        return best_move, counter

    def get_legal_moves(self):
        moves = ChessEngine.generate_moves(self.board)
        legal_moves = ChessEngine.filter_illegal_moves(self.board, moves)
        return legal_moves

    def perform_move(self, move):
        if move in self.currentLegalMoves:
            ChessEngine.perform_move(move, self.board, move_type="binary", with_validation=False, move_actually_executed=True)
            self.move_number += 1
        else:
            print("Valid input, but invalid move. Enter a move of the form a1a2 (start square->destination square).")


if __name__ == "__main__":
    board = ChessBoard()
    # board.load_from_fen("r1bqk2r/pp1p1pQp/3bp3/8/3nP3/P7/1PP1K1PP/RNB2BNR w HAkq - 0 1")
    game = ChessGame(board, max_depth = 4, time_limit = 5, isBlackAI=False, isWhiteAI=True, isBlackStockfishAI=True, isWhiteStockfishAI=False)
    game.play()
    
    # service = ChessPrintService()
    # board = ChessBoard()
    # board.load_from_fen("8/8/8/4k3/8/8/3K2R1/1R6 w - - 0 1")
    # score = board.evaluate_board()
    # print(score)
    # service.print_board(board.bitboards)
    # print(board.evaluate_board())
