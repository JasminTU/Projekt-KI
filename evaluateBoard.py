

def evaluate(board):
    """
    Evaluates the given chess board and returns a score representing the current state of the game.
    :param board: the chess board as an 8x8 bitboard.
    :return: a score representing the current state of the game.
    """
    score = 0
    for i in range(64):
        piece_value = piece_value_at(board, i)
        if get_color_at(board, i) == 'W':
            score += piece_value
        if get_color_at(board, i) == 'B':
            score -= piece_value
    return score


def get_color_at(board, i):
    """
    Returns the color of the piece at the given position on the board.
    :param board: the chess board as an 8x8 bitboard.
    :param i: the position to check, represented as an integer between 0 and 63.
    :return: the color of the piece at the given position, either 'W' for white or 'B' for black.
    """
    white_pieces = board['W']
    black_pieces = board['B']
    mask = 1 << i

    if white_pieces & mask:
        return 'W'
    elif black_pieces & mask:
        return 'B'
    else:
        return None


def get_piece_at(i):
    """
    Gibt die Schachfigur an der i-ten Position des Schachbretts zurück.
    :param i: eine Ganzzahl zwischen 0 und 63, die die Position des Bits im Bitboard angibt.
    :return: eine Zeichenkette, die die Schachfigur an dieser Position repräsentiert, oder None, wenn keine Figur vorhanden ist.
    """
    # Konvertiere die i-te Position in eine (row, column) Koordinate
    row = i // 8
    col = i % 8

    # Definiere die Schachfiguren als Bitmasken
    pawn = 0b0000000100000000
    knight = 0b0000001000000000
    bishop = 0b0000010000000000
    rook = 0b0000100000000000
    queen = 0b0001000000000000
    king = 0b0010000000000000

    # Überprüfe, ob die Position i die entsprechende Schachfigur repräsentiert
    if pawn & (1 << i):
        return 'P'
    elif knight & (1 << i):
        return 'N'
    elif bishop & (1 << i):
        return 'B'
    elif rook & (1 << i):
        return 'R'
    elif queen & (1 << i):
        return 'Q'
    elif king & (1 << i):
        return 'K'
    else:
        return None

def piece_value_at(board, position):
    """
    Returns the value of the piece at the given position on the board.
    :param board: the chess board as an 8x8 bitboard.
    :param position: the position to check, represented as an integer between 0 and 63.
    :return: the value of the piece at the given position.
    """
    piece_values = {
        'P': 1,
        'N': 3,
        'B': 3,
        'R': 5,
        'Q': 9,
        'K': 100
    } # dictionary containing the values of each piece

    piece = get_piece_at(board, position)
    if piece is not None:
        return piece_values[piece]
    else:
        return 0
