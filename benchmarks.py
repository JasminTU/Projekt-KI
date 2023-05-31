from ChessEngine import ChessEngine
from ChessBoard import ChessBoard
import time


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
            max_depth = 4
            best_move, counter = board.iterative_depth_search(max_depth)

            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time

        average_time = total_time * 1000 / num_tests
        average_time = round(average_time, 4)  # Round to 4 decimal places
        print(f"FEN: {fen}")
        print(f"Average time per test: {average_time} milliseconds\n")

    def benchmark_fen1(self):
        fen1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w"
        self.benchmark_chess_engine(fen1)

    def benchmark_fen2(self):
        fen2 = "8/8/4kpp1/3p4/p6P/2B4b/6P1/6K1 w - - 1 48"
        self.benchmark_chess_engine(fen2)

    def benchmark_fen3(self):
        fen3 = "5rk1/pp4pp/4p3/2R3Q1/3n4/6qr/P1P2PPP/5RK1 w - - 2 24"
        self.benchmark_chess_engine(fen3)


if __name__ == "__main__":
    benchmark = ChessEngineBenchmark()
    benchmark.benchmark_fen1()
    benchmark.benchmark_fen2()
    benchmark.benchmark_fen3()
