from ChessEngine import ChessEngine
from ChessBoard import ChessBoard
import time

from ChessGame import ChessGame


class ChessEngineBenchmark:
    def __init__(self):
        pass

    @staticmethod
    def benchmark_chess_engine(fen):
        total_time = 0.0
        num_tests = 1000

        for _ in range(num_tests):
            board = ChessBoard()
            board.load_from_fen(fen)

            start_time = time.time()

            # Your chess engine implementation
            moves = ChessEngine.generate_moves(board)
            moves = ChessEngine.filter_illegal_moves(board, moves)

            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time

        average_time = total_time * 1000 / num_tests
        average_time = round(average_time, 4)  # Round to 4 decimal places
        print(f"FEN: {fen}")
        print(f"Average time per test: {average_time} milliseconds\n")

    @staticmethod
    def benchmark_chess_engine_alpha_beta(fen, depth, with_cut_off=True):
        total_time = 0.0
        num_tests = 1

        if with_cut_off:
            print("Alpha-Beta")
        else:
            print("MinMax")
        print(f"FEN: {fen}")
        
        for _ in range(num_tests):
            board = ChessBoard()
            board.load_from_fen(fen)
            game = ChessGame(board, isBlackAI=True, isWhiteAI=True)

            start_time = time.time()

            # process_next_move() calls iterative_depth_search()
            move, counter = game.process_next_move(depth, print_board=False, with_cut_off=with_cut_off, time_limit=10, with_time_limit=False)

            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time

        average_time = total_time / num_tests
        average_time = round(average_time, 4)  # Round to 4 decimal places
        print(f"Depth: {depth}")
        print(f"Counter: {counter}")
        print(f"Best Move: {ChessEngine.binary_move_to_algebraic(move[0], move[1])}")
        print(f"Time: {average_time:.4f} seconds\n")

    def benchmark_fen1(self):
        fen1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
        self.benchmark_chess_engine(fen1)

    def benchmark_fen2(self):
        fen2 = "8/8/4kpp1/3p4/p6P/2B4b/6P1/6K1 w - - 1 48"
        self.benchmark_chess_engine(fen2)

    def benchmark_fen3(self):
        fen3 = "5rk1/pp4pp/4p3/2R3Q1/3n4/6qr/P1P2PPP/5RK1 w - - 2 24"
        self.benchmark_chess_engine(fen3)

    def benchmark_fen_alpha_beta1(self):
        fen1 = "r1bqk1nr/8/2n3P1/p1bP3p/3pPPQ1/p1N5/8/R1B1KBNR b KQkq - 0 1"
        self.benchmark_chess_engine_alpha_beta(fen1, depth=3)

    def benchmark_fen_alpha_beta2(self):
        fen2 = "rnbqkbnr/p1pppppp/8/1p6/Q7/2P5/PP1PPPPP/RNB1KBNR w KQkq - 0 1"
        self.benchmark_chess_engine_alpha_beta(fen2, depth=3)

    def benchmark_fen_alpha_beta3(self):
        fen3 = "r1bqk1nr/8/2n3P1/p1bP3p/3pPPQ1/p1N5/8/R1B1KBNR b KQkq - 0 1"
        self.benchmark_chess_engine_alpha_beta(fen3, depth=4)

    def benchmark_fen_alpha_beta4(self):
        fen4 = "rnbqkbnr/p1pppppp/8/1p6/Q7/2P5/PP1PPPPP/RNB1KBNR w KQkq - 0 1"
        self.benchmark_chess_engine_alpha_beta(fen4, depth=4)



if __name__ == "__main__":
    benchmark = ChessEngineBenchmark()
    benchmark.benchmark_fen_alpha_beta1()
    benchmark.benchmark_fen_alpha_beta2()
    benchmark.benchmark_fen_alpha_beta3()
    benchmark.benchmark_fen_alpha_beta4()
