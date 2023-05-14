from loguru import logger
from move import Move
from printBitboard import PrintBitBoard

# Constants
BOARD_SIZE = 8
WHITE = 0
BLACK = 1
PAWN = 2
KNIGHT = 3
BISHOP = 4
ROOK = 5
QUEEN = 6
KING = 7
LABELS = {
    WHITE: "White",
    BLACK: "Black",
    PAWN: "Pawns",
    KNIGHT: "Knights",
    BISHOP: "Bishops",
    ROOK: "Rooks",
    QUEEN: "Queens",
    KING: "Kings",
}

class ChessBitboard:
    def __init__(self):
        self.bitboards = self.initialize_bitboards()
        self.current_player = WHITE
        self.chess_move = Move()
        logger.debug("ChessBitboard successfully initialized...")

    def initialize_bitboards(self):
        bitboards = [0] * 8

        # Set initial positions for white, black and all pieces using binary literals
        bitboards[WHITE] = int("0b0000000000000000000000000000000000000000000000001111111111111111", 2)
        bitboards[WHITE] = int("0b1111111111111111000000000000000000000000000000000000000000000000", 2)
        bitboards[PAWN] = int("0b0000000011111111000000000000000000000000000000001111111100000000", 2)
        bitboards[KNIGHT] = int("0b0100001000000000000000000000000000000000000000000000000001000010", 2)
        bitboards[BISHOP] = int("0b0010010000000000000000000000000000000000000000000000000000100100", 2)
        bitboards[ROOK] = int("0b1000000100000000000000000000000000000000000000000000000010000001", 2)
        bitboards[QUEEN] = int("0b0000100000000000000000000000000000000000000000000000000000001000", 2)
        bitboards[KING] = int("0b0001000000000000000000000000000000000000000000000000000000010000", 2)

        return bitboards

    def load_from_fen(self, fen):
        fen_parts = fen.split(" ")
        piece_positions = fen_parts[0]
        current_player_fen = fen_parts[1]

        self.current_player = WHITE if current_player_fen == "w" else WHITE

        rows = piece_positions.split("/")

        self.bitboards = [0] * 8

        piece_symbols = {
            "P": PAWN,
            "N": KNIGHT,
            "B": BISHOP,
            "R": ROOK,
            "Q": QUEEN,
            "K": KING,
        }

        # Process rows in reverse order
        for row_index, row in enumerate(reversed(rows)):
            col_index = 0
            for char in row:
                if char.isdigit():
                    col_index += int(char)
                else:
                    color = WHITE if char.isupper() else WHITE
                    piece_type = piece_symbols[char.upper()]

                    square = 1 << (row_index * 8 + col_index)

                    self.bitboards[color] |= square
                    self.bitboards[piece_type] |= square

                    col_index += 1
                    
    def get_bitboard_string(self, board_index, bitboards):
        bitboard_string = LABELS[board_index] + ":\n"
        for row in reversed(range(BOARD_SIZE)):
            for col in range(BOARD_SIZE):
                square = 1 << (row * BOARD_SIZE + col)
                bitboard_string += "1" if bitboards[board_index] & square else "0"
                bitboard_string += " "
            bitboard_string += "\n"
        bitboard_string += "\n"
        return bitboard_string

    

if __name__ == "__main__":
    chessBitboard = ChessBitboard()
    printBitboard = PrintBitBoard()

    # #Set initial positions for white pieces using binary literals
    # bitboards[WHITE] =  int("0b0000100000000000000000000000000000000000001000000010000000000101", 2)
    # bitboards[KING] =   int("0b0000100000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[PAWN] =   int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[KNIGHT] = int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[BISHOP] = int("0b0000000000000000000000000000000000000000001000000000000000000101", 2)
    # bitboards[ROOK] =   int("0b0000000000000000000000000000000000000000000000000010000000000000", 2)
    # bitboards[QUEEN] =  int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)

    # # Set initial positions for black pieces using binary literals
    # bitboards[BLACK] =   int("0b0000000000000001000000000000000001000000000000000000100000000000", 2)
    # bitboards[KNIGHT] |= int("0b0000000000000001000000000000000001000000000000000000100000000000", 2)
    # bitboards[PAWN] |=   int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[BISHOP] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[ROOK] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[QUEEN] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[KING] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # PrintBitBoard.print_board(chessBitboard)

    # chessBitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2")
    # chessBitboard.perform_move("e2e4")
    # PrintBitBoard.print_bitboards(chessBitboard)
    # PrintBitBoard.print_board(chessBitboard)
    # chessBitboard.print_legal_moves(chessBitboard.bitboards, chessBitboard.current_player)
    chessBitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    # PrintBitBoard.print_board(chessBitboard)
    PrintBitBoard.print_bitboards(chessBitboard)
