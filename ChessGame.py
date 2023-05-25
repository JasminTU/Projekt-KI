from ChessPrintService import ChessPrintService
from ChessBoard import ChessBoard
from ChessEngine import ChessEngine
import constants
import re
from loguru import logger
import sys


class ChessGame:
    def __init__(self, board, isBlackAI=True, isWhiteAI=False):
        self.board = board
        self.move_number = 1
        self.isBlackAI = isBlackAI
        self.isWhiteAI = isWhiteAI
        self.currentLegalMoves = []

    def play(self):
        while True:
            self.print_board()
            self.currentLegalMoves = self.get_legal_moves()
            # Check for draw and checkmate before the move is exercised
            if self.is_draw():  # more detailed print is in draw function
                break

            if self.is_ai_turn():
                move = self.get_ai_move()
            else:
                move = ChessEngine.algebraic_move_to_binary(self.get_human_move())

            self.perform_move(move)
            
            if self.opponent_is_check_mate() or ChessEngine.player_is_king_on_the_hill(self.board):
                winner = "White" if self.board.game_result == constants.WHITE else "Black"
                print("Checkmate! Winner is ", winner)
                break


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

    def get_ai_move(self):

        if len(self.currentLegalMoves) == 0:
            logger.error("List is empty. This case should be captured as a check mate or draw!")
            return sys.exit(1)
        best_move = self.board.iterative_depth_search(4)
        # bestMove = None
        # bestScore = None
        # for move in self.currentLegalMoves:
        #     score = self.board.evaluate_board(move, move_type="binary")
        #     if not bestScore or bestScore < score:
        #         bestScore = score
        #         bestMove = move
        str = "White" if self.board.current_player == constants.WHITE else "Black"
        print(f"Move {self.move_number} by {str} (AI): {ChessEngine.binary_move_to_algebraic(best_move[0], best_move[1])}")
        return best_move

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

    def opponent_is_check_mate(self):
        return ChessEngine.opponent_is_check_mate(self.board)

    def is_draw(self):
        return ChessEngine.is_draw(self.currentLegalMoves, self.board)


if __name__ == "__main__":
    game = ChessGame(ChessBoard(), isBlackAI=True, isWhiteAI=True)
    game.play()
