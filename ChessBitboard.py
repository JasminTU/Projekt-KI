from loguru import logger
from move import Move
from printBitboard import PrintBitBoard
import constants

class ChessBitboard:
    def __init__(self):
        self.bitboards = self.initialize_bitboards()
        self.current_player = constants.WHITE
        self.chess_move = Move()

    def initialize_bitboards(self):
        bitboards = [0] * 8

        # Set initial positions for constants.WHITE, black and all pieces using binary literals
        bitboards[constants.WHITE] =  int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
        bitboards[constants.BLACK] =  int("0b1111111111111111000000000000000000000000000000000000000000000000", 2)
        bitboards[constants.PAWN] =   int("0b0000000011111111000000000000000000000000000000001111111100000000", 2)
        bitboards[constants.KNIGHT] = int("0b0100001000000000000000000000000000000000000000000000000001000010", 2)
        bitboards[constants.BISHOP] = int("0b0010010000000000000000000000000000000000000000000000000000100100", 2)
        bitboards[constants.ROOK] =   int("0b1000000100000000000000000000000000000000000000000000000010000001", 2)
        bitboards[constants.QUEEN] =  int("0b0000100000000000000000000000000000000000000000000000000000001000", 2)
        bitboards[constants.KING] =   int("0b0001000000000000000000000000000000000000000000000000000000010000", 2)

        return bitboards

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
                    
    def get_bitboard_string(self, board_index):
        bitboard_string = constants.LABELS[board_index] + ":\n"
        for row in reversed(range(constants.BOARD_SIZE)):
            for col in range(constants.BOARD_SIZE):
                square = 1 << (row * constants.BOARD_SIZE + col)
                bitboard_string += "1" if self.bitboards[board_index] & square else "0"
                bitboard_string += " "
            bitboard_string += "\n"
        bitboard_string += "\n"
        return bitboard_string

    

if __name__ == "__main__":
    ChessBitboard = ChessBitboard()
    printBitboard = PrintBitBoard()


    # chessBitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2")
    # chessBitboard.perform_move("e2e4")
    # PrintBitBoard.print_bitboards(chessBitboard)
    # PrintBitBoard.print_board(chessBitboard)
    # chessBitboard.print_legal_moves(chessBitboard.bitboards, chessBitboard.current_player)
    # chessBitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    # PrintBitBoard.print_board(chessBitboard)
    
    # printBitboard.print_bitboards(chessBitboard.bitboards)
    printBitboard.print_board(ChessBitboard.bitboards)
