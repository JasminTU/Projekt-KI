import PrintBitboardService
from ChessBitboard import ChessBitboard


class ChessGame:
    def __init__(self, board):
        self.board = board
        self.chess_engine = board.chess_move
        self.move_number = 1

    def play(self):
        while True:
            self.print_board()
            move = self.get_move()
            if not move:
                print("Invalid input. Try again.")
                continue
            if not self.perform_move(move):
                print("Invalid move. Try again.")
                continue
            if self.is_checkmate():
                print("Checkmate!")
                break
            self.move_number += 1

    def print_board(self):
        PrintBitboardService.PrintBitBoardService.print_board(self.board.bitboards)

    def get_move(self):
        user_input = input(f"Move {self.move_number}: ")
        if len(user_input) == 4:
            return user_input
        else:
            return None

    def perform_move(self, move):
        try:
            self.chess_engine.perform_move(move, self.board)
            return True
        except Exception:
            return False

    def is_checkmate(self):
        return self.board.is_check_mate()


if __name__ == "__main__":
    chess_engine = ChessBitboard()
    game = ChessGame(chess_engine)
    game.play()
