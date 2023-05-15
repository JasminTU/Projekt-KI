import unittest
from ChessBitboard import ChessBitboard
from illegalMoveException import IllegalMoveException
import constants
from PrintBitboardService import PrintBitBoardService

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
    def setUp(self):
        self.expectedBoard = ChessBitboard()
        self.actualBoard = ChessBitboard()

    def assertEqualBitboards(self, exptectedBoard, actualBoard):
        """
        This method compares the expected bitboards to the actual bitboards and raises an AssertionError if they are not equal.
        :param exptectedBoard: the exptectedBoard to compare.
        :param actualBoard: the actualBoard to compare.
        """
        board_index = 0
        try:
            for i in range(constants.KING + 1):
                board_index = i
                self.assertEqual(exptectedBoard.bitboards[i], actualBoard.bitboards[i])
        except AssertionError:
            error_message = f"{constants.LABELS.get(board_index)} Bitboard is not equal:\n"
            error_message += "\nExpected:\n"
            error_message += PrintBitBoardService.get_bitboard_string(board_index, exptectedBoard.bitboards)
            error_message += "\nActual:\n"
            error_message += PrintBitBoardService.get_bitboard_string(board_index, actualBoard.bitboards)
            raise AssertionError(error_message)


    def assertIsInCheck(self, actualBoard):
        """
        This method checks whether a given board is in check and raises an AssertionError if it is not.
        :param actualBoard: the actualBoard to check.
        """
        try:
            self.assertTrue(actualBoard.is_in_check(actualBoard.current_player))
        except AssertionError:
            error_message = f"There should be a check on the following board, but none were found:\n\n"
            error_message += PrintBitBoardService.get_board_string(actualBoard.bitboards)
            raise AssertionError(error_message)

    def assertIsNotInCheck(self, actualBoard):
        """
        This method checks whether a given board is not in check and raises an AssertionError if it.
        :param actualBoard: the actualBoard to check.
        """
        try:
            self.assertFalse(actualBoard.is_in_check(actualBoard.current_player))
        except AssertionError:
            error_message = f"There should be no check on the following board, but at least one was found:\n\n"
            error_message += PrintBitBoardService.get_board_string(actualBoard.bitboards)
            raise AssertionError(error_message)


    def test_initial_board(self):
        self.actualBoard.initialize_bitboards()
        self.expectedBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_legal_1(self):
        self.actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.actualBoard.chess_move.perform_move('e2e4', self.actualBoard, move_type = "algebraic")
        self.expectedBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_legal_2(self):
        self.actualBoard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
        self.actualBoard.chess_move.perform_move('d4e5', self.actualBoard, move_type = "algebraic")
        self.expectedBoard.load_from_fen("rnbqkbnr/pppp1ppp/8/4P3/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_legal_3(self):
        self.actualBoard.load_from_fen("rnbqk1nr/pppp1ppp/4p3/2b5/3P4/4P3/PPP2PPP/RNBQKBNR w KQkq - 0 1")
        self.actualBoard.chess_move.perform_move('d4c5', self.actualBoard, move_type = "algebraic")
        self.expectedBoard.load_from_fen("rnbqk1nr/pppp1ppp/4p3/2P5/8/4P3/PPP2PPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_legal_4(self):
        self.actualBoard.load_from_fen("rnbqkbnr/ppppppp1/8/7p/P7/8/1PPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, self.actualBoard.chess_move.perform_move, 'a4h5', self.actualBoard)

    def test_move_pawn_legal_5(self):
        self.actualBoard.load_from_fen("rn1qkbnr/ppp1pppp/8/3p4/8/7b/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.actualBoard.chess_move.perform_move('g2h3', self.actualBoard, move_type = "algebraic")
        self.expectedBoard.load_from_fen("rn1qkbnr/ppp1pppp/8/3p4/8/7P/PPPPPP1P/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)

    def test_move_pawn_legal_6(self):
        self.actualBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/3P4/6q1/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
        self.actualBoard.chess_move.perform_move('f2g3', self.actualBoard, move_type = "algebraic")
        self.expectedBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/3P4/6P1/PPP1P1PP/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)


    def test_move_pawn_illegal_1(self):
        self.assertRaises(IllegalMoveException, self.actualBoard.chess_move.perform_move, 'e7e5', self.actualBoard, move_type = "algebraic")

    def test_en_passant(self):
        self.actualBoard.load_from_fen("4k3/8/8/4pP2/8/8/8/4K3 w - e6 0 2")
        self.actualBoard.chess_move.perform_move('f5e6', self.actualBoard, move_type = "algebraic")
        self.expectedBoard.load_from_fen("4k3/8/4P3/8/8/8/8/4K3 b - - 0 2")
        self.assertEqualBitboards(self.expectedBoard, self.actualBoard)
    
    def test_en_pessant_illegal_1(self):
        self.actualBoard.load_from_fen("4k3/8/8/3pP3/8/8/8/4K3 w - - 0 2")
        self.assertRaises(IllegalMoveException, self.actualBoard.chess_move.perform_move, 'e5d6', self.actualBoard)

    def test_en_pessant_illegal_2(self):
        self.actualBoard.load_from_fen("4k3/8/5P2/4p3/8/8/8/4K3 w - e6 0 2")
        self.assertRaises(IllegalMoveException, self.actualBoard.chess_move.perform_move, 'f6e6', self.actualBoard)

    def test_evaluate_board_initial(self):
        self.actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(self.actualBoard.evaluate_board(), 0)

    def test_evaluate_board_on_pawn(self):
        self.actualBoard.load_from_fen("rnbqkbnr/pp1ppppp/8/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        boardScore = self.actualBoard.evaluate_board()

    def test_evaluate_board_on_rook(self):
        self.actualBoard.load_from_fen("1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/1NBQKBNR w Kk - 0 1")
        self.assertEqual(self.actualBoard.evaluate_board(), 0)

    def test_evaluate_board_on_bishop(self):
        self.actualBoard.load_from_fen("1n1qkbnr/pppppppp/8/8/8/R1r5/PPPPPPPP/1N1QKBNR w Kk - 0 1")
        self.assertEqual(self.actualBoard.evaluate_board(), 0)

    def test_evaluate_board_on_queen(self):
        self.actualBoard.load_from_fen("5p2/8/8/8/8/8/4Q3/7P w - - 0 1")
        self.assertEqual(self.actualBoard.evaluate_board(), 900)

    def test_evaluate_board_on_king(self):
        self.actualBoard.load_from_fen("1n2kbnr/pppppppp/2b5/8/8/R1r2Bq1/PPPPPPPP/1N1Q1BNR w Hk - 0 1")
        self.assertEqual(self.actualBoard.evaluate_board(), -2000)

    def test_evaluate_board_on_empty(self):
        self.actualBoard.load_from_fen("8/8/8/8/8/8/8/8 w - - 0 1")
        self.assertEqual(self.actualBoard.evaluate_board(), 0)

    def test_is_in_check_1(self):
        self.actualBoard.load_from_fen("rnbq1bnr/ppp1pppp/4k3/8/8/8/PPP1QPPP/RNBK1BNR w KQha - 0 1")
        self.assertIsInCheck(self.actualBoard)

    def test_is_in_check_2(self):
        self.actualBoard.load_from_fen("rnbq1bnr/pppkpppp/8/8/8/8/PPP2PPP/RNBQKBNR w KQha - 0 1")
        self.assertIsNotInCheck(self.actualBoard)

    def test_is_in_check_3(self):
        self.actualBoard.load_from_fen("rnbqkb1r/pppnpppp/8/8/6K1/8/PPP2PPP/RNB1QBNR w HAkq - 0 1")
        self.assertIsNotInCheck(self.actualBoard)

    def test_is_in_check_4(self):
        self.actualBoard.load_from_fen("rnbqkb1r/pppnpppp/8/6K1/8/8/PPP2PPP/RNB1QBNR w HAkq - 0 1")
        self.assertIsNotInCheck(self.actualBoard)

    def test_is_in_check_7(self):
        self.actualBoard.load_from_fen("rnbqkb1r/pppnppp1/7p/6K1/8/8/PPP2PPP/RNB1QBNR w HAkq - 0 1")
        self.assertIsInCheck(self.actualBoard)

    def test_is_in_check_5(self):
        self.actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/5P2/6K1/8/PPP3PP/RNB1QBNR w HAkq - 0 1")
        # Test schlägt Fehl, weil der Läufer irrtümlich durch das Pferd läuft
        self.assertIsNotInCheck(self.actualBoard)

    def test_is_in_check_6(self):
        self.actualBoard.load_from_fen("rnbqknbr/ppp1pppp/4K3/5P2/8/8/PPP3PP/RNB1QBNR w HAkq - 0 1")
        self.assertIsInCheck(self.actualBoard)


if __name__ == '__main__':
    unittest.main()
