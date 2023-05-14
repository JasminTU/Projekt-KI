import chessBitboard

class PrintBitBoard():
    
    def __init__(self) -> None:
        pass
    
    def print_bitboard(self, message, bitboard):
        # print a single bitboard in a 8x8 grid
        print(message, "\n")
        for row in range(7, -1, -1):
            for col in range(8):
                index = row * 8 + col
                if bitboard & (1 << index):
                    print("1", end=" ")
                else:
                    print("0", end=" ")
            print()
        print("--------\n")
        
    def print_bitboards(self, bitboards):
        bitboards_string = ""

        for i, _ in enumerate(bitboards):
            bitboards_string += self._get_bitboard_string(i, bitboards)

        print(bitboards_string)
        
    def _get_bitboard_string(self, board_index, bitboards):
        bitboard_string = chessBitboard.LABELS[board_index] + ":\n"
        for row in reversed(range(chessBitboard.BOARD_SIZE)):
            for col in range(chessBitboard.BOARD_SIZE):
                square = 1 << (row * chessBitboard.BOARD_SIZE + col)
                bitboard_string += "1" if bitboards[board_index] & square else "0"
                bitboard_string += " "
            bitboard_string += "\n"
        bitboard_string += "\n"
        return bitboard_string
        
    def print_board(self, bitboards):
        piece_symbols = {
            (chessBitboard.WHITE, chessBitboard.PAWN): "P",
            (chessBitboard.WHITE, chessBitboard.KNIGHT): "N",
            (chessBitboard.WHITE, chessBitboard.BISHOP): "B",
            (chessBitboard.WHITE, chessBitboard.ROOK): "R",
            (chessBitboard.WHITE, chessBitboard.QUEEN): "Q",
            (chessBitboard.WHITE, chessBitboard.KING): "K",
            (chessBitboard.BLACK, chessBitboard.PAWN): "p",
            (chessBitboard.BLACK, chessBitboard.KNIGHT): "n",
            (chessBitboard.BLACK, chessBitboard.BISHOP): "b",
            (chessBitboard.BLACK, chessBitboard.ROOK): "r",
            (chessBitboard.BLACK, chessBitboard.QUEEN): "q",
            (chessBitboard.BLACK, chessBitboard.KING): "k",
        }

        board_string = ""

        for row in reversed(range(chessBitboard.BOARD_SIZE)):
            for col in range(chessBitboard.BOARD_SIZE):
                square = 1 << (row * chessBitboard.BOARD_SIZE + col)
                piece = None
                color = (
                    chessBitboard.WHITE
                    if bitboards[chessBitboard.WHITE] & square
                    else chessBitboard.BLACK
                    if bitboards[chessBitboard.BLACK] & square
                    else None
                )

                if color is not None:
                    for piece_type in range(chessBitboard.PAWN, chessBitboard.KING + 1):
                        if bitboards[piece_type] & square:
                            piece = piece_symbols[(color, piece_type)]
                            break

                board_string += piece if piece else "."
                board_string += " "
            board_string += f"| {8 - row}\n"
        board_string += f"" + "-" * 15 + f"\n"
        board_string += f"a b c d e f g h\n\n"

        print(board_string)