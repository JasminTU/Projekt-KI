from ChessBoard import ChessBoard
from ChessGame import ChessGame
import ChessEngine
import constants
from stockfish_get_eval_score import KingOfTheHillAIScore
import time

dataset = []

class DatasetGenerator(ChessGame):
    def __init__(self, board, max_depth, time_limit, isBlackAI=True, isWhiteAI=True, isBlackStockfishAI=False, isWhiteStockfishAI=False):
        super().__init__(board, max_depth, time_limit, isBlackAI, isWhiteAI, isBlackStockfishAI, isWhiteStockfishAI)
    
    def process_next_move(self, print_board=True, with_cut_off=True, with_time_limit = True):
        if print_board:
            self.print_board()
        self.currentLegalMoves = self.get_legal_moves()
        # Check for draw and checkmate before the move is exercised
        if ChessEngine.is_draw(self.currentLegalMoves, self.board):  # more detailed print is in draw function
            return "draw", None
        if ChessEngine.is_game_over(self.board) or ChessEngine.is_game_won(self.board):
            winner = "White" if self.board.game_result == constants.WHITE else "Black"
            print("Checkmate! Winner is ", winner)
            return "checkmate", None

        if self.is_ai_turn():
            move, counter = self.get_ai_move(print_board, with_cut_off, with_time_limit)
        elif self.is_stockfish_ai_turn():
            move = ChessEngine.algebraic_move_to_binary(self.get_stockfish_move())
            counter = -1
        else:
            move = ChessEngine.algebraic_move_to_binary(self.get_human_move())
            counter = -1

        stockfish_ai_score = KingOfTheHillAIScore()
        evaluation_score = stockfish_ai_score.get_evaluation_score()
        king_square = self.get_king_square()
        dataset.append((self.board.bitboards, move, self.board.current_player, evaluation_score, king_square))

        self.perform_move(move)
        self.board.previous_moves.append(ChessEngine.binary_move_to_algebraic(move[0], move[1]))
        return move, counter
    
    def get_king_square(self):
        return self.board.bitboards[self.board.current_player] | self.board.bitboards[constants.KING]

if __name__ == "__main__":
    start_time = time.time()
    while(True):
        board = ChessBoard()
        game = ChessGame(board, max_depth = 4, time_limit = 1, isBlackAI=False, isWhiteAI=False, isBlackStockfishAI=True, isWhiteStockfishAI=True)
        game.play()

        elapsed_time = time.time() - start_time
        if elapsed_time > 20:
            break