""" 
Important stockfish commands:
https://github.com/official-stockfish/Stockfish/wiki/Commands#standard-commands
https://github.com/fairy-stockfish/Fairy-Stockfish/wiki/Command-line
"""
import os
import subprocess

if os.name == "posix":  # Linux or macOS
    fairy_stockfish_path = os.path.join(os.path.dirname(__file__), "fairy-stockfish-largeboard_x86-64")
elif os.name == "nt":  # Windows
    fairy_stockfish_path = os.path.join(os.path.dirname(__file__), "fairy-stockfish-largeboard_x86-64.exe")
else:
    raise OSError("Unsupported operating system.")

# Use fairy_stockfish_path in your code

class KingOfTheHillAI():
    def __init__(self) -> None:
        self.engine = None

    def get_best_move(self, board, time_limit):
        best_move = None
        # Create the subprocess to communicate with Fairy-Stockfish
        self.engine = subprocess.Popen(
            fairy_stockfish_path,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
        # Set the protocol
        self.engine.stdin.write("uci\n")

        # Set the chess variant
        self.engine.stdin.write("setoption name UCI_Variant value kingofthehill\n")

        # Set the board position in Fairy-Stockfish
        moves_string = " ".join(board.previous_moves)
        self.engine.stdin.write(f"position startpos moves {moves_string}\n")

        # Request the best move from Fairy-Stockfish in x milliseconds
        time_limit *= 1000
        self.engine.stdin.write(f"go movetime {time_limit}\n")
        self.engine.stdin.flush()

        # Read the output lines until the line with the best move is found
        while True:
            line = self.engine.stdout.readline().strip()
            if line.startswith("bestmove"):
                best_move = line.split()[1]
                break
            
        # Close the engine subprocess
        self.engine.stdin.write("quit\n")
        self.engine.stdin.close()
        self.engine.wait()

        return best_move



