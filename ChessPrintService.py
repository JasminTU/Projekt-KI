import constants


class ChessPrintService:

    def __init__(self) -> None:
        pass

    @staticmethod
    def get_bitboards_string(bitboards):
        bitboards_string = ""
        for i, _ in enumerate(bitboards):
            bitboards_string += ChessPrintService.get_bitboard_string(i, bitboards)
        return bitboards_string

    @staticmethod
    def print_bitboards(bitboards):
        print(ChessPrintService.get_bitboards_string(bitboards))

    @staticmethod
    def get_bitboard_string(board_index, bitboards):
        bitboard_string = constants.LABELS[board_index] + ":\n"
        for row in reversed(range(constants.BOARD_SIZE)):
            for col in range(constants.BOARD_SIZE):
                square = 1 << (row * constants.BOARD_SIZE + col)
                bitboard_string += "1" if bitboards[board_index] & square else "0"
                bitboard_string += " "
            bitboard_string += "\n"
        bitboard_string += "\n"
        return bitboard_string

    @staticmethod
    def print_bitboard(board_index, bitboard):
        ChessPrintService.get_bitboard_string(board_index, bitboard)
        
    @staticmethod
    def print_binary_bitboard(bitboard):
        for rank in range(7, -1, -1):
            for file in range(8):
                square = rank * 8 + file
                if bitboard & (1 << square):
                    print("1", end=" ")
                else:
                    print("0", end=" ")
            print()
        print("\n")

    @staticmethod
    def get_board_string(bitboards):
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
            board_string += f"| {row + 1}\n"
        board_string += f"" + "-" * 15 + f"\n"
        board_string += f"a b c d e f g h\n\n"

        return board_string

    @staticmethod
    def print_board(bitboards):
        print(ChessPrintService.get_board_string(bitboards))
