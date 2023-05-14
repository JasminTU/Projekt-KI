import constants

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
        bitboard_string = constants.LABELS[board_index] + ":\n"
        for row in reversed(range(constants.BOARD_SIZE)):
            for col in range(constants.BOARD_SIZE):
                square = 1 << (row * constants.BOARD_SIZE + col)
                bitboard_string += "1" if bitboards[board_index] & square else "0"
                bitboard_string += " "
            bitboard_string += "\n"
        bitboard_string += "\n"
        return bitboard_string
        
    def print_board(self, bitboards):
        piece_symbols = {
            (constants.WHITE, constants.PAWN): "P",
            (constants.WHITE, constants.KNIGHT): "N",
            (constants.WHITE, constants.BISHOP): "B",
            (constants.WHITE, constants.ROOK): "R",
            (constants.WHITE, constants.QUEEN): "Q",
            (constants.WHITE, constants.KING): "K",
            (constants.BLACK, constants.PAWN): "p",
            (constants.BLACK, constants.KNIGHT): "n",
            (constants.BLACK, constants.BISHOP): "b",
            (constants.BLACK, constants.ROOK): "r",
            (constants.BLACK, constants.QUEEN): "q",
            (constants.BLACK, constants.KING): "k",
        }

        board_string = ""

        for row in reversed(range(constants.BOARD_SIZE)):
            for col in range(constants.BOARD_SIZE):
                square = 1 << (row * constants.BOARD_SIZE + col)
                piece = None
                color = (
                    constants.WHITE
                    if bitboards[constants.WHITE] & square
                    else constants.BLACK
                    if bitboards[constants.BLACK] & square
                    else None
                )

                if color is not None:
                    for piece_type in range(constants.PAWN, constants.KING + 1):
                        if bitboards[piece_type] & square:
                            piece = piece_symbols[(color, piece_type)]
                            break

                board_string += piece if piece else "."
                board_string += " "
            board_string += f"| {8 - row}\n"
        board_string += f"" + "-" * 15 + f"\n"
        board_string += f"a b c d e f g h\n\n"

        print(board_string)