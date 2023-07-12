# Here's a modified version of the DatasetGenerator class that integrates with your ChessGame class.
import numpy as np

import ChessBoard
from ChessGame import ChessGame
from stockfish_get_eval_score import KingOfTheHillAIScore


class DatasetGenerator:
    def __init__(self, chess_game, random_move_chance=0.1):
        """
        Initialize the dataset generator.

        Parameters:
        - chess_game: An instance of the ChessGame class.
        - random_move_chance: The chance to make a random move instead of the best move.
        """
        self.chess_game = chess_game
        self.random_move_chance = random_move_chance

    def generate_dataset(self, num_games):
        """
        Generate a dataset by having the AI play games against itself.

        Parameters:
        - num_games: The number of games to play.

        Returns:
        - A list of game records, where each record is a tuple of (features, label).
        """
        dataset = []

        for _ in range(num_games):
            dataset.extend(self._play_game())

        return dataset

    def _play_game(self):
        """
        Play a single game and return the game record.

        Returns:
        - A list of position records, where each record is a tuple of (features, label).
        """
        game_record = []

        while True:
            result, _ = self.chess_game.process_next_move(print_board=False)

            if result == "checkmate" or result == "draw":
                break

            features = self._extract_features()
            label = self._get_evaluation_score()
            game_record.append((features, label))

        return game_record

    def _extract_features(self):
        """Extract features from the board."""
        # Please replace this with your actual feature extraction code.
        return None

    def _get_evaluation_score(self):
        """Get the evaluation score for the board."""
        return KingOfTheHillAIScore.get_evaluation_score(self.chess_game.board, 1)

    def _make_move(self):
        """Make a move on the board."""
        if np.random.random() < self.random_move_chance:
            move = self._get_random_move()
        else:
            move = self.chess_game.get_best_move(print_move=False)

        self.chess_game.perform_move(move)

    def _get_random_move(self):
        """Get a random legal move."""
        legal_moves = self.chess_game.get_legal_moves()
        return np.random.choice(legal_moves)

# To use this class, you'd create an instance of the ChessGame class and pass it to the DatasetGenerator constructor:
board = ChessBoard.ChessBoard()
chess_game = ChessGame(board, time_limit = 1)
generator = DatasetGenerator(chess_game, random_move_chance=0.1)
# Then you can generate a dataset:
dataset = generator.generate_dataset(num_games=10)
