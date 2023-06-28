from ChessPrintService import ChessPrintService
from ChessBoard import ChessBoard
from ChessEngine import ChessEngine
import constants
import re
from loguru import logger
import sys


class ChessGame:
    def __init__(self, board, isBlackAI=True, isWhiteAI=True):
        self.board = board
        self.move_number = 1
        self.isBlackAI = isBlackAI
        self.isWhiteAI = isWhiteAI
        self.currentLegalMoves = []

    def play(self):
        while True:
            if self.process_next_move() == "checkmate" or self.process_next_move() == "draw":
                break

    def process_next_move(self, max_depth=3, print_board=True, with_cut_off=True):
        if print_board:
            self.print_board()
        self.currentLegalMoves = self.get_legal_moves()
        # Check for draw and checkmate before the move is exercised
        if ChessEngine.is_draw(self.currentLegalMoves, self.board):  # more detailed print is in draw function
            return "draw"
        if ChessEngine.is_check_mate(self.board) or ChessEngine.opponent_is_king_on_the_hill(self.board):
            winner = "White" if self.board.game_result == constants.WHITE else "Black"
            print("Checkmate! Winner is ", winner)
            return "checkmate"

        if self.is_ai_turn():
            move, counter = self.get_ai_move(max_depth, print_board, with_cut_off)
        else:
            move = ChessEngine.algebraic_move_to_binary(self.get_human_move())

        self.perform_move(move)


    def print_board(self):
        ChessPrintService.print_board(self.board.bitboards)

    def is_ai_turn(self):
        return (self.isWhiteAI and self.move_number % 2 == constants.BLACK) or (
                self.isBlackAI and self.move_number % 2 == constants.WHITE)

    def get_human_move(self):
        str = "White" if self.board.current_player == constants.WHITE else "Black"
        user_input = input(f"Move {self.move_number} by {str}: ")
        while not self.validate_input(user_input):
            print("Invalid input. Enter a move of the form a1a2 (start square->destination square).")
            user_input = input(f"Move {self.move_number} by {str}: ")
        return user_input

    def validate_input(self, user_input):
        pattern = r'^[a-h][1-8][a-h][1-8]$'
        return re.match(pattern, user_input) is not None

    def get_ai_move(self, max_depth, print_move=True, with_cut_off=True):

        if len(self.currentLegalMoves) == 0:
            logger.error("List is empty. This case should be captured as a check mate or draw!")
            sys.exit(1)
        best_move, counter = self.board.iterative_depth_search(max_depth, with_cut_off)
        str = "White" if self.board.current_player == constants.WHITE else "Black"
        if print_move:
            print(f"Move {self.move_number} by {str} (AI): {ChessEngine.binary_move_to_algebraic(best_move[0], best_move[1])}")
        return best_move, counter

    def get_legal_moves(self):
        moves = ChessEngine.generate_moves(self.board)
        legal_moves = ChessEngine.filter_illegal_moves(self.board, moves)
        return legal_moves

    def perform_move(self, move):
        if move in self.currentLegalMoves:
            ChessEngine.perform_move(move, self.board, move_type="binary", with_validation=False)
            self.move_number += 1
        else:
            print("Valid input, but invalid move. Enter a move of the form a1a2 (start square->destination square).")


if __name__ == "__main__":
    board = ChessBoard()
    # board.load_from_fen("2Q5/R5p1/5k1p/2p5/4pB2/2N5/1P4PP/5K1R w - - 0 1")
    game = ChessGame(board, isBlackAI=True, isWhiteAI=True)
    game.play()
    
    # service = ChessPrintService()
    # board = ChessBoard()
    # board.load_from_fen("8/8/8/4k3/8/8/3K2R1/1R6 w - - 0 1")
    # score = board.evaluate_board()
    # print(score)
    # service.print_board(board.bitboards)
    # print(board.evaluate_board())
