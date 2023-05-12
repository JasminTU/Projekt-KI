import unittest
from ChessBitboard import ChessBitboard
from ChessBitboard import IllegalMoveException


class TestChessBitboard(unittest.TestCase):
    """
    This class contains unit tests for the ChessBitboard class.

    It tests functionality such as board initialization, piece movement,
    check/checkmate detection, and game rules enforcement, among other
    operations relevant to the chess game.

    Each method in this class is a separate test case. These test cases
    can be run individually or collectively to verify the correctness of
    the ChessBitboard class.

    Test boards can be generated using the fen notation using the following website: https://lichess.org/editor
    """

    def assertEqualBitboards(self, exptectedBoard, actualBoard):
        """
        This method compares the expected bitboards to the actual bitboards and raises an AssertionError if they are not equal.
        :param exptectedBoard: the exptectedBoard to compare.
        :param actualBoard: the actualBoard to compare.
        """
        board_index = 0
        try:
            for i in range(exptectedBoard.KING + 1):
                board_index = i
                self.assertEqual(exptectedBoard.bitboards[i], actualBoard.bitboards[i])
        except AssertionError:
            error_message = f"{exptectedBoard.labels.get(board_index)} Bitboard is not equal:\n"
            error_message += "\nExpected:\n"
            error_message += exptectedBoard.get_bitboard_string(board_index)
            error_message += "\nActual:\n"
            error_message += actualBoard.get_bitboard_string(board_index)
            raise AssertionError(error_message)

    def setUp(self):
        self.expectedBoard = ChessBitboard()
        self.actualBoard = ChessBitboard()

    def test_initial_board(self):
        self.actualBoard.initialize_bitboards()
        self.expectedBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_legal_1(self):
        self.actualBoard.perform_move('e2e4')
        self.expectedBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_legal_2(self):
        self.actualBoard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
        self.actualBoard.perform_move('d4e5')
        self.expectedBoard.load_from_fen("rnbqkbnr/pppp1ppp/8/4P3/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_legal_3(self):
        self.actualBoard.load_from_fen("rnbqk1nr/pppp1ppp/4p3/2b5/3P4/4P3/PPP2PPP/RNBQKBNR w KQkq - 0 1")
        self.actualBoard.perform_move('d4c5')
        self.expectedBoard.load_from_fen("rnbqk1nr/pppp1ppp/4p3/2P5/8/4P3/PPP2PPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_illegal_1(self):
        self.assertRaises(IllegalMoveException, self.actualBoard.perform_move, 'e7e5')


if __name__ == '__main__':
    unittest.main()
