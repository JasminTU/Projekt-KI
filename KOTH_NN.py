import chess
import numpy as np
import tensorflow as tf


class KingOfTheHillNeuralNetwork:

    def __init__(self):
        self.model = None
        self.piece_to_index = {
            "P": 0,
            "N": 1,
            "B": 2,
            "R": 3,
            "Q": 4,
            "K": 5
        }

    def residual_block(self, x, filters, strides):
        shortcut = x
        x = tf.keras.layers.Conv2D(
            filters, (3, 3), strides=strides, padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.ReLU()(x)
        x = tf.keras.layers.Conv2D(
            filters, (3, 3), strides=1, padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        if strides != 1:
            shortcut = tf.keras.layers.Conv2D(
                filters, (1, 1), strides=strides, padding='same')(shortcut)
            shortcut = tf.keras.layers.BatchNormalization()(shortcut)
        x = tf.keras.layers.add([x, shortcut])
        x = tf.keras.layers.ReLU()(x)
        return x

    def build_model(self, input_shape):
        inputs = tf.keras.layers.Input(shape=input_shape)
        x = tf.keras.layers.Conv2D(
            32, (3, 3), strides=1, padding='same')(inputs)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.ReLU()(x)
        x = self.residual_block(x, 32, 1)
        x = self.residual_block(x, 32, 1)
        x = self.residual_block(x, 64, 2)
        x = self.residual_block(x, 64, 1)
        x = self.residual_block(x, 128, 2)
        x = self.residual_block(x, 128, 1)
        x = tf.keras.layers.Flatten()(x)
        x = tf.keras.layers.Dense(256, activation='relu')(x)
        outputs = tf.keras.layers.Dense(1)(x)
        self.model = tf.keras.models.Model(inputs, outputs)

    def compile_model(self):
        optimizer = tf.keras.optimizers.Adam()
        self.model.compile(optimizer=optimizer,
                           loss=self.king_of_the_hill_loss)

    def king_of_the_hill_loss(self, y_true, y_pred):
        return tf.keras.losses.mean_squared_error(y_true, y_pred)

    def train(self, pgn_files, batch_size=32, epochs=10):
        boards = []
        results = []
        for pgn_file in pgn_files:
            with open(pgn_file) as f:
                game = chess.pgn.read_game(f)
                board = game.board()
                for move in game.mainline_moves():
                    board.push(move)
                    if board.is_variant_draw():
                        result = 0
                    elif board.king(color=chess.WHITE) in board.pieces(chess.KING, chess.BLACK) and board.is_checkmate():
                        result = -1
                    elif board.king(color=chess.BLACK) in board.pieces(chess.KING, chess.WHITE) and board.is_checkmate():
                        result = 1
                    else:
                        result = 0
                    boards.append(board.copy())
                    results.append(result)

        features = np.zeros((len(boards), 8, 8, 6))
        labels = np.array(results)
        for i, board in enumerate(boards):
            for r in range(8):
                for c in range(8):
                    piece = board.piece_at(chess.square(r, c))
                    if piece is not None:
                        features[i, r, c,
                                 self.piece_to_index[piece.symbol()]] = 1

        self.model.fit(features, labels, batch_size=batch_size,
                       epochs=epochs, shuffle=True)

    def get_best_move(self, board):
        # Get the features for the current board position
        features = np.zeros((1, 8, 8, 6))
        for r in range(8):
            for c in range(8):
                piece = board.piece_at(chess.square(r, c))
                if piece is not None:
                    features[0, r, c, self.piece_to_index[piece.symbol()]] = 1

        # Predict the value of each possible move
        move_values = {}
        for move in board.legal_moves:
            board.push(move)
            if board.is_variant_draw():
                result = 0
            elif board.king(color=chess.WHITE) in board.pieces(chess.KING, chess.BLACK) and board.is_checkmate():
                result = -1
            elif board.king(color=chess.BLACK) in board.pieces(chess.KING, chess.WHITE) and board.is_checkmate():
                result = 1
            else:
                features_next = np.zeros((1, 8, 8, 6))
                for r in range(8):
                    for c in range(8):
                        piece = board.piece_at(chess.square(r, c))
                        if piece is not None:
                            features_next[0, r, c,
                                          self.piece_to_index[piece.symbol()]] = 1
                result = self.model.predict(features_next)[0]

            board.pop()
            move_values[move] = result

        # Choose the best move
        best_move = max(move_values, key=move_values.get)
        return best_move


if __name__ == "__main__":
    # list of your own PGN files that you want to use to train the mode
    pgn_files = ["game1.pgn", "game2.pgn", "game3.pgn"]
    model = KingOfTheHillNeuralNetwork()
    model.build_model((8, 8, 6))
    model.compile_model()
    model.train(pgn_files)

    # Example board position
    example_board = chess.Board("4k3/4p3/4K3/8/8/8/8/8 w - - 0 1")

    # Get the best move for the given board position
    best_move = model.get_best_move(example_board)
    # https://www.ficsgames.org/download.html
    # Print the best move
    print("Best move:", best_move.uci())
