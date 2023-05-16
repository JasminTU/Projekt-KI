from loguru import logger
from move import Move
from PrintBitboardService import PrintBitBoardService
import constants
import copy

class ChessBitboard:
    def __init__(self):
        self.bitboards = None
        self.initialize_bitboards()
        self.current_player = constants.WHITE
        self.chess_move = Move()
        self.next_player_in_check = False

    def initialize_bitboards(self):
        self.bitboards = [0] * 8

        # Set initial positions for constants.WHITE, black and all pieces using binary literals
        self.bitboards[constants.WHITE] =  int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
        self.bitboards[constants.BLACK] =  int("0b1111111111111111000000000000000000000000000000000000000000000000", 2)
        self.bitboards[constants.PAWN] =   int("0b0000000011111111000000000000000000000000000000001111111100000000", 2)
        self.bitboards[constants.KNIGHT] = int("0b0100001000000000000000000000000000000000000000000000000001000010", 2)
        self.bitboards[constants.BISHOP] = int("0b0010010000000000000000000000000000000000000000000000000000100100", 2)
        self.bitboards[constants.ROOK] =   int("0b1000000100000000000000000000000000000000000000000000000010000001", 2)
        self.bitboards[constants.QUEEN] =  int("0b0000100000000000000000000000000000000000000000000000000000001000", 2)
        self.bitboards[constants.KING] =   int("0b0001000000000000000000000000000000000000000000000000000000010000", 2)

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

    def evaluate_board(self):
        score = 0
        opponent = constants.BLACK if self.current_player == constants.WHITE else constants.WHITE
        # Evaluate material value: chatgpt constants
        # score += 1 * (bin(self.bitboards[constants.PAWN] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.PAWN] & self.bitboards[opponent]).count("1"))
        # score += 3 * (bin(self.bitboards[constants.KNIGHT] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.KNIGHT] & self.bitboards[opponent]).count("1"))
        # score += 3 * (bin(self.bitboards[constants.BISHOP] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.BISHOP] & self.bitboards[opponent]).count("1"))
        # score += 5 * (bin(self.bitboards[constants.ROOK] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.ROOK] & self.bitboards[opponent]).count("1"))
        # score += 9 * (bin(self.bitboards[constants.QUEEN] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.QUEEN] & self.bitboards[opponent]).count("1"))

        # Evaluate material value: slide constants (pawns are differetiated)
        score += 50 * (bin(self.bitboards[constants.PAWN] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.PAWN] & self.bitboards[opponent]).count("1"))
        score += 300 * (bin(self.bitboards[constants.KNIGHT] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.KNIGHT] & self.bitboards[opponent]).count("1"))
        score += 300 * (bin(self.bitboards[constants.BISHOP] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.BISHOP] & self.bitboards[opponent]).count("1"))
        score += 500 * (bin(self.bitboards[constants.ROOK] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.ROOK] & self.bitboards[opponent]).count("1"))
        score += 900 * (bin(self.bitboards[constants.QUEEN] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.QUEEN] & self.bitboards[opponent]).count("1"))
        score += 2000 * (bin(self.bitboards[constants.KING] & self.bitboards[self.current_player]).count("1") - bin(self.bitboards[constants.KING] & self.bitboards[opponent]).count("1"))

        # Evaluate position of kings
        # king_pos = bin(self.bitboards[constants.KING] & self.bitboards[self.current_player]).count("1")
        # if king_pos in range(4, 12) or king_pos in range(52, 60): # define some range in the center of the field
        #     score += 3
        return score
    
    def is_in_check(self , player):
        # move is a tuple containing start and destination bitboards, checks if input player is in check
        # TODO: king - king face off not included yet
        legal_moves_opponent = self.chess_move.generate_legal_moves(self.bitboards, self._get_opponent(player))
        dest_legal_moves = [elem[1] for elem in legal_moves_opponent]
        in_check = [dest & (self.bitboards[constants.KING] & self.bitboards[player]) for dest in dest_legal_moves]
        return any(elem != 0 for elem in in_check)

    def _get_opponent(self, current_player):
        return constants.WHITE if current_player == constants.BLACK else constants.BLACK

    def is_check_mate(self):
        if not self.is_in_check(self.current_player):
            return False
        legal_moves = self.chess_move.generate_legal_moves(self.bitboards, self.current_player)
        for move in legal_moves:
            board_after_move = copy.deepcopy(self)
            board_after_move.chess_move.perform_move(move, board_after_move, move_type="binary")
            if not board_after_move.is_in_check(self.current_player):
                return False
        return True

if __name__ == "__main__":
    actualBoard = ChessBitboard()
    actualBoard.load_from_fen("rnbqkbnr/8/7B/8/8/8/8/RN1QKBNR w KQkq - 0 1")
    # actualBoard.chess_move.print_legal_moves(actualBoard.bitboards, actualBoard.current_player)
    actualBoard.chess_move.perform_move('h6f8', actualBoard)
