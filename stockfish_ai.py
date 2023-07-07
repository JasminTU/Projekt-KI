""" 
Important stockfish commands:
https://github.com/official-stockfish/Stockfish/wiki/Commands#standard-commands
https://github.com/fairy-stockfish/Fairy-Stockfish/wiki/Command-line
"""
import subprocess

# Specify the path to the Fairy-Stockfish executable
fairy_stockfish_path = r"C:\Users\Xello\Documents\Informatik\Module\Schach-KI\Projekt-KI\fairy-stockfish-largeboard_x86-64.exe"


class KingOfTheHillAI():
    def __init__(self) -> None:
        # Create the subprocess to communicate with Fairy-Stockfish
        self.engine = subprocess.Popen(
            fairy_stockfish_path,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )
    def get_best_move(self, board):


# Set up the initial board state for King of the Hill
board_state = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1"

# Set the protocol
self.engine.stdin.write("uci\n")

# Set the chess variant
self.engine.stdin.write("setoption name UCI_Variant value kingofthehill\n")

# Set the board position in Fairy-Stockfish
self.engine.stdin.write(f"position fen {board_state}\n")

# Request the best move from Fairy-Stockfish in x milliseconds
self.engine.stdin.write("go movetime 2000\n")
self.engine.stdin.flush()

# # To perform the move
# self.engine.stdin.write("position fen \"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1\" moves e2e4\n")

# Read the output lines until the line with the best move is found
while True:
    line = self.engine.stdout.readline().strip()
    if line.startswith("bestmove"):
        best_move = line.split()[1]
        break

# Print the best move
print("Best move:", best_move)

# Close the engine subprocess
self.engine.stdin.write("quit\n")
self.engine.stdin.close()
self.engine.wait()


