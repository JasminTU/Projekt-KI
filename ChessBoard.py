from ChessEngine import ChessEngine
from ChessPrintService import ChessPrintService
import constants
import copy


class ChessBoard:
    def __init__(self):
        self.bitboards = None
        self.initialize_bitboards()
        self.current_player = constants.WHITE
        self.next_player_in_check = False
        self.game_result = None
        self.board_history = []

    def initialize_bitboards(self):
        self.bitboards = [0] * 8

        # Set initial positions for constants.WHITE, black and all pieces using binary literals
        self.bitboards[constants.WHITE] = int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
        self.bitboards[constants.BLACK] = int("0b1111111111111111000000000000000000000000000000000000000000000000", 2)
        self.bitboards[constants.PAWN] = int("0b0000000011111111000000000000000000000000000000001111111100000000", 2)
        self.bitboards[constants.KNIGHT] = int("0b0100001000000000000000000000000000000000000000000000000001000010", 2)
        self.bitboards[constants.BISHOP] = int("0b0010010000000000000000000000000000000000000000000000000000100100", 2)
        self.bitboards[constants.ROOK] = int("0b1000000100000000000000000000000000000000000000000000000010000001", 2)
        self.bitboards[constants.QUEEN] = int("0b0000100000000000000000000000000000000000000000000000000000001000", 2)
        self.bitboards[constants.KING] = int("0b0001000000000000000000000000000000000000000000000000000000010000", 2)

    def load_from_fen(self, fen):
        fen_parts = fen.split(" ")
        piece_positions = fen_parts[0]
        current_player_fen = fen_parts[1]

        self.current_player = constants.WHITE if current_player_fen == "w" else constants.BLACK

        rows = piece_positions.split("/")

        self.bitboards = [0] * 8

        piece_symbols = {
            "P": constants.PAWN,
            "N": constants.KNIGHT,
            "B": constants.BISHOP,
            "R": constants.ROOK,
            "Q": constants.QUEEN,
            "K": constants.KING,
        }

        # Process rows in reverse order
        for row_index, row in enumerate(reversed(rows)):
            col_index = 0
            for char in row:
                if char.isdigit():
                    col_index += int(char)
                else:
                    color = constants.WHITE if char.isupper() else constants.BLACK
                    piece_type = piece_symbols[char.upper()]

                    square = 1 << (row_index * 8 + col_index)

                    self.bitboards[color] |= square
                    self.bitboards[piece_type] |= square

                    col_index += 1
        # PrintBitBoardService.print_bitboards(self.bitboards)
        # PrintBitBoardService.print_board(self.bitboards)

    def evaluate_board(self, move=None, move_type="algebraic"):
        # evaluate the board after a move or on current board
        board_after_move = copy.deepcopy(self)
        if move:
            board_after_move.chess_move.perform_move(move, board_after_move, move_type, with_validation=False)

        score = 0
        opponent = constants.BLACK if self.current_player == constants.WHITE else constants.WHITE

        # Evaluate material value: slide constants (pawns are differentiated)
        score += 50 * (
                bin(board_after_move.bitboards[constants.PAWN] & board_after_move.bitboards[self.current_player]).count(
                    "1") - bin(board_after_move.bitboards[constants.PAWN] & board_after_move.bitboards[opponent]).count(
                "1"))
        score += 300 * (bin(
            board_after_move.bitboards[constants.KNIGHT] & board_after_move.bitboards[self.current_player]).count(
            "1") - bin(board_after_move.bitboards[constants.KNIGHT] & board_after_move.bitboards[opponent]).count("1"))
        score += 300 * (bin(
            board_after_move.bitboards[constants.BISHOP] & board_after_move.bitboards[self.current_player]).count(
            "1") - bin(self.bitboards[constants.BISHOP] & board_after_move.bitboards[opponent]).count("1"))
        score += 500 * (
                bin(board_after_move.bitboards[constants.ROOK] & board_after_move.bitboards[self.current_player]).count(
                    "1") - bin(board_after_move.bitboards[constants.ROOK] & board_after_move.bitboards[opponent]).count(
                "1"))
        score += 900 * (bin(
            board_after_move.bitboards[constants.QUEEN] & board_after_move.bitboards[self.current_player]).count(
            "1") - bin(board_after_move.bitboards[constants.QUEEN] & board_after_move.bitboards[opponent]).count("1"))
        score += 2000 * (
                bin(board_after_move.bitboards[constants.KING] & board_after_move.bitboards[self.current_player]).count(
                    "1") - bin(board_after_move.bitboards[constants.KING] & board_after_move.bitboards[opponent]).count(
                "1"))

        # Evaluate position of kings
        # king_pos = bin(self.bitboards[constants.KING] & self.bitboards[self.current_player]).count("1")
        # if king_pos in range(4, 12) or king_pos in range(52, 60): # define some range in the center of the field
        #     score += 3
        return score

    @staticmethod
    def get_opponent(player):
        return constants.WHITE if player == constants.BLACK else constants.BLACK


if __name__ == "__main__":
    service = ChessPrintService()
    expectedBoard = ChessBoard()
    actualBoard = ChessBoard()
    actualBoard.load_from_fen("rnbq1bnr/8/7k/8/8/B1R5/8/RN1QKB2 w Qa - 0 1")
    king_moves = ChessEngine.get_move_by_figure(actualBoard.bitboards, actualBoard.current_player, constants.BISHOP)
    for move in king_moves:
        alg = ChessEngine.binary_move_to_algebraic(move[0], move[1])
        print(alg)
    # actualBoard.chess_move.print_legal_moves(actualBoard)
