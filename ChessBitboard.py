from loguru import logger
from move import Move
from PrintBitboardService import PrintBitBoardService
import constants

class ChessBitboard:
    def __init__(self):
        self.bitboards = self.initialize_bitboards()
        self.current_player = constants.WHITE
        self.chess_move = Move()
        self.next_player_in_check = False

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
    
    def is_in_check(self):
        # move is a tuple containing start and destination bitboards
        # TODO: king - king face off not included yet
        legal_moves_opponent = self.chess_move.generate_legal_moves(self.bitboards, self._get_opponent(self.current_player))
        dest_legal_moves = [elem[1] for elem in legal_moves_opponent]
        in_check = [dest & (self.bitboards[constants.KING] & self.bitboards[self.current_player]) for dest in dest_legal_moves]
        return any(elem != 0 for elem in in_check)
    
    def _get_opponent(self, current_player):
        return constants.WHITE if current_player == constants.BLACK else constants.BLACK
        
if __name__ == "__main__":
    chessBitboard = ChessBitboard()


    chessBitboard.load_from_fen("rnbq1bnr/pppkpppp/8/8/8/8/PPP2PPP/RNBQKBNR w KQha - 0 1")
    # printBitboard.print_bitboards(chessBitboard.bitboards)
    in_check = chessBitboard.is_in_check()
    print(in_check)
    # for elem in in_check:
    #     printBitboard.print_bitboard(".", elem)
    # print(in_check)
    # chessBitboard.perform_move("e2e4")
    # PrintBitBoard.print_board(chessBitboard)
    # chessBitboard.chess_move.print_legal_moves(chessBitboard.bitboards, chessBitboard._get_opponent(chessBitboard.current_player))
    # chessBitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    # PrintBitBoard.print_board(chessBitboard)
    
    # printBitboard.print_bitboards(chessBitboard.bitboards)
    # printBitboard.print_board(ChessBitboard.bitboards)
