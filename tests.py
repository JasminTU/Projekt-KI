import unittest
from ChessBitboard import ChessBitboard

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

    def assert_equal_bitboards(self, bitboard1, bitboard2):
        """
        This method compares two bitboards and raises an AssertionError if they are not equal.
        :param bitboard1: the first bitboard to compare.
        :param bitboard2: the second bitboard to compare.
        """
        try:
            self.assertEqual(bitboard1.bitboards, bitboard2.bitboards)
        except AssertionError:
            error_message = "Bitboards are not equal:"
            error_message += "\nBitboard:\n"
            error_message += bitboard1.get_board_string()
            error_message += "\nTestboard:\n"
            error_message += bitboard2.get_board_string()
            raise AssertionError(error_message)

    def setUp(self):
        self.testboard = ChessBitboard()
        self.bitboard = ChessBitboard()

    def test_initial_board(self):
        self.bitboard.initialize_bitboards()
        self.testboard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(self.bitboard.bitboards, self.testboard.bitboards)

    def test_move_pawn_legal_1(self):
        self.bitboard.perform_move('e2e4')
        self.testboard.load_from_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqual(self.bitboard.bitboards, self.testboard.bitboards)
    def test_move_pawn_legal_2(self):
        self.bitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
        self.bitboard.perform_move('d4e5')
        self.testboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4P3/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1")
        self.assert_equal_bitboards(self.bitboard, self.testboard)
    def test_move_pawn_illegal_1(self):
        self.assertRaises(Exception, self.bitboard.perform_move, 'e7e5')

if __name__ == '__main__':
    unittest.main()
