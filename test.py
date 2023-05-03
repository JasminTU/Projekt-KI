import chess.pgn


def test1():
    # Open a PGN file
    with open("game.pgn") as pgn_file:
        # Read the first game from the file
        game = chess.pgn.read_game(pgn_file)

        # Print the mainline moves of the game
        for move in game.mainline_moves():
            print(move)


def test2():
    # Open a PGN file
    with open("game.pgn") as pgn_file:
        # Read the first game from the file
        game = chess.pgn.read_game(pgn_file)

        # Create a chess board object representing the starting position of the game
        board = game.board()
        for move in game.mainline_moves():
            print(move)
            board.push(move)
            print(board)


test2()
