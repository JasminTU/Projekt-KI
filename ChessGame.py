import random
from PrintBitboardService import PrintBitBoardService
from ChessBitboard import ChessBitboard


class ChessGame:
    def __init__(self, board, isBlackAI=True, isWhiteAI=False):
        self.board = board
        self.chess_engine = board.chess_move
        self.move_number = 1
        self.isBlackAI = isBlackAI
        self.isWhiteAI = isWhiteAI
        self.currentLegalMoves = []

    def play(self):
        while True:
            self.print_board()
            if self.is_ai_turn():
                move = self.get_ai_move()
            else:
                move = self.chess_engine.algebraic_move_to_binary(self.get_human_move())
            if not move:
                print("Invalid input. Try again.")
                continue
            if not self.perform_move(move):
                print("Invalid move. Try again.")
                continue
            if self.is_checkmate():
                print("Checkmate!")
                break
            if self.is_draw():
                print("Draw!")
                break
            self.move_number += 1

    def print_board(self):
        PrintBitBoardService.print_board(self.board.bitboards)

    def is_ai_turn(self):
        return (self.isWhiteAI and self.move_number % 2 == 1) or (self.isBlackAI and self.move_number % 2 == 0)

    def get_human_move(self):
        user_input = input(f"Move {self.move_number}: ")
        if len(user_input) == 4:
            return user_input
        else:
            return None

    def get_ai_move(self):
        moves = self.chess_engine.generate_moves(self.board)
        legal_moves = self.chess_engine.filter_illegal_moves(self.board, moves)
        self.currentLegalMoves = legal_moves
        return random.choice(legal_moves)

    def perform_move(self, move):
        try:
            self.chess_engine.perform_move(move, self.board, move_type="binary")
            return True
        except Exception:
            return False

    def is_checkmate(self):
        return self.board.is_check_mate()

    def is_draw(self):
        return self.chess_engine.is_draw(self.currentLegalMoves, self.board)


if __name__ == "__main__":
    chess_engine = ChessBitboard()
    game = ChessGame(chess_engine, isBlackAI=True, isWhiteAI=True)
    game.play()
