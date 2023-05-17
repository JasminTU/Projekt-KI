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

    def assertEqualBitboards(self, expectedBoard, actualBoard):
        """
        This method compares the expected bitboards to the actual bitboards and raises an AssertionError if they are not equal.
        :param expectedBoard: the expectedBoard to compare.
        :param actualBoard: the actualBoard to compare.
        """
        board_index = 0
        try:
            for i in range(constants.KING + 1):
                board_index = i
                self.assertEqual(expectedBoard.bitboards[i], actualBoard.bitboards[i])
        except AssertionError:
            error_message = f"{constants.LABELS.get(board_index)} Bitboard is not equal:\n"
            error_message += "\nExpected:\n"
            error_message += PrintBitBoardService.get_bitboard_string(board_index, expectedBoard.bitboards)
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
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        expectedBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_king_legal_1(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkBnr/8/8/8/8/8/8/RN1QKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move((constants.E1, constants.F2), actualBoard, move_type="binary")
        expectedBoard.load_from_fen("rnbqkBnr/8/8/8/8/8/5K2/RN1Q1BNR w HAkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_king_legal_2(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkBnr/8/8/8/8/8/8/RN1QKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('e1e2', actualBoard)
        expectedBoard.load_from_fen("rnbqkBnr/8/8/8/8/8/4K3/RN1Q1BNR w HAkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_king_legal_3(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkBnr/8/8/2NNN3/2RKB3/4B3/8/RN1Q4 w Akq - 0 1")
        actualBoard.chess_move.perform_move('d4c3', actualBoard)
        expectedBoard.load_from_fen("rnbqkBnr/8/8/2NNN3/2R1B3/2K1B3/8/RN1Q4 w Akq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_king_illegal_1(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'e1d1', actualBoard)

    def test_move_king_illegal_2(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'g2f3', actualBoard)


    def test_move_king_illegal_3(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'f4e5', actualBoard)

    def test_move_king_illegal_4(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'e2f2', actualBoard)

    def test_move_king_illegal_5(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkBnr/8/8/4N3/1N2B3/1K2B3/R7/RN1Q4 w Akq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'b3a4', actualBoard)

    def test_move_king_illegal_6(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbq1bnr/8/B6k/8/8/B1R5/8/RN1QK3 b Qha - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'h6a6', actualBoard)
        
    def test_move_king_illegal_7(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbq1bnr/8/k6B/8/8/B1R5/8/RN1QK3 b Qha - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'a6h6', actualBoard)

    def test_move_king_illegal_8(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbq1bnr/8/7k/8/8/B1R5/8/RN1QKB2 b Qha - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'h6a6', actualBoard)

    def test_move_pawn_legal_2(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('d4e5', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/pppp1ppp/8/4P3/8/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_pawn_legal_3(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqk1nr/pppp1ppp/4p3/2b5/3P4/4P3/PPP2PPP/RNBQKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('d4c5', actualBoard)
        expectedBoard.load_from_fen("rnbqk1nr/pppp1ppp/4p3/2P5/8/4P3/PPP2PPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_pawn_legal_4(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppppppp1/8/7p/P7/8/1PPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'a4h5', actualBoard)

    def test_move_pawn_legal_5(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rn1qkbnr/ppp1pppp/8/3p4/8/7b/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('g2h3', actualBoard)
        expectedBoard.load_from_fen("rn1qkbnr/ppp1pppp/8/3p4/8/7P/PPPPPP1P/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_pawn_legal_6(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/3P4/6q1/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('f2g3', actualBoard)
        expectedBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/3P4/6P1/PPP1P1PP/RNBQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)


    def test_move_pawn_legal_7(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('d7d6', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/ppp1pppp/3p4/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_pawn_legal_8(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('d7d5', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3p4/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    #black capturing seems to be broken(left)
    def test_move_pawn_legal_9(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppppppp1/8/7p/P5P1/8/1PPPPP1P/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('h5g4', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/ppppppp1/8/8/P5p1/8/1PPPPP1P/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    # black capturing seems to be broken(right)
    def test_move_pawn_legal_10(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppppp1pp/8/5p2/6P1/8/PPPPPP1P/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('f5g4', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/ppppp1pp/8/8/6p1/8/PPPPPP1P/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_pawn_illegal_1(self):
        actualBoard = ChessBitboard()
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'e7e5', actualBoard)

    def test_move_pawn_illegal_2(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'e7f6', actualBoard)

    def test_move_pawn_illegal_3(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'h5a4', actualBoard)

    def test_evaluate_board_initial(self):
        actualBoard = ChessBitboard()
        actualBoard.initialize_bitboards()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(0, actualBoard.evaluate_board())

    def test_evaluate_board_on_pawn(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pp1ppppp/8/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(0, actualBoard.evaluate_board())

    def test_evaluate_board_on_rook(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1nbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/1NBQKBNR w Kk - 0 1")
        self.assertEqual(0, actualBoard.evaluate_board())

    def test_evaluate_board_on_bishop(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1n1qkbnr/pppppppp/8/8/8/R1r5/PPPPPPPP/1N1QKBNR w Kk - 0 1")
        self.assertEqual(0, actualBoard.evaluate_board())

    def test_evaluate_board_on_queen(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("5p2/8/8/8/8/8/4Q3/7P w - - 0 1")
        self.assertEqual(900, actualBoard.evaluate_board())

    def test_evaluate_board_on_king(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1n2kbnr/pppppppp/2b5/8/8/R1r2Bq1/PPPPPPPP/1N1Q1BNR w Hk - 0 1")
        self.assertEqual(-2000, actualBoard.evaluate_board())

    def test_move_rook_legal_1(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/8/8/8/3R4/8/8/1NBQKBNR w Kkq - 0 1")
        actualBoard.chess_move.perform_move('d4d6', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/8/3R4/8/8/8/8/1NBQKBNR w Kkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_rook_legal_2(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/8/8/8/3R4/8/8/1NBQKBNR w Kkq - 0 1")
        actualBoard.chess_move.perform_move('d4h4', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/8/8/8/7R/8/8/1NBQKBNR w Kkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_rook_legal_3(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/8/3q4/8/3R4/8/8/1NBQKBNR w Kkq - 0 1")
        actualBoard.chess_move.perform_move('d4d6', actualBoard)
        expectedBoard.load_from_fen("rnb1kbnr/8/3R4/8/8/8/8/1NBQKBNR w Kkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_rook_legal_4(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbn1/ppppppp1/8/7r/8/8/PPPPPPPP/RNBQKBNR b KQq - 0 1")
        actualBoard.chess_move.perform_move('h5h4', actualBoard)
        expectedBoard.load_from_fen("rnbqkbn1/ppppppp1/8/8/7r/8/PPPPPPPP/RNBQKBNR b KQq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_rook_legal_5(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbn1/ppppppp1/8/8/7r/8/PPPPPPPP/RNBQKBNR b KQq - 0 1")
        actualBoard.chess_move.perform_move('h4e4', actualBoard)
        expectedBoard.load_from_fen("rnbqkbn1/ppppppp1/8/8/4r3/8/PPPPPPPP/RNBQKBNR b KQq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_rook_legal_6(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbn1/ppppppp1/8/8/5P1r/8/PPPPP1PP/RNBQKBNR b KQq - 0 1")
        actualBoard.chess_move.perform_move('h4f4', actualBoard)
        expectedBoard.load_from_fen("rnbqkbn1/ppppppp1/8/8/5r2/8/PPPPP1PP/RNBQKBNR b KQq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_rook_legal_7(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbn1/ppppppp1/8/3N1r2/8/8/PPPPP1PP/R1BQKBNR b KQq - 0 1")
        actualBoard.chess_move.perform_move('f5d5', actualBoard)
        expectedBoard.load_from_fen("rnbqkbn1/ppppppp1/8/3r4/8/8/PPPPP1PP/R1BQKBNR b KQq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_rook_illegal_1(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/8/3R4/8/8/8/8/1NBQKBNR w Kkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd6e7', actualBoard)


    def test_rook_illegal_2(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/8/3R4/8/8/8/8/1NBQKBNR w Kkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd6f4', actualBoard)


    def test_rook_illegal_3(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1k1nr/8/3R4/4b3/8/8/8/1NBQKBNR w Kkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd6e5', actualBoard)

    def test_rook_illegal_4(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'a1a2', actualBoard)

    def test_rook_illegal_5(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/R7/8/1PPPPPPP/1NBQKBNR w Kkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'a4c5', actualBoard)

    def test_rook_illegal_6(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbn1/ppppppp1/8/3r4/8/8/PPPPP1PP/R1BQKBNR b KQq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd5c4', actualBoard)

    def test_rook_illegal_7(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'h8h7', actualBoard)

    def test_rook_illegal_8(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'h8a8', actualBoard)

    def test_move_bishop_legal_1(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('c1h6', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/8/7B/8/8/8/8/RN1QKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_bishop_legal_2(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/8/7B/8/8/8/8/RN1QKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('h6f8', actualBoard)
        expectedBoard.load_from_fen("rnbqkBnr/8/8/8/8/8/8/RN1QKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_bishop_legal_3(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppp1p/6p1/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('f8h6', actualBoard)
        expectedBoard.load_from_fen("rnbqk1nr/pppppp1p/6pb/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_bishop_legal_4(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqk1nr/pppppp1p/6pb/8/5P2/8/PPPPP1PP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('h6f4', actualBoard)
        expectedBoard.load_from_fen("rnbqk1nr/pppppp1p/6p1/8/5b2/8/PPPPP1PP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_bishop_illegal_1(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqk1nr/8/7B/8/8/8/8/RN1QKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'h6g6', actualBoard)

    def test_bishop_illegal_2(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqk1nr/8/7B/8/8/8/8/RN1QKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'c1d2', actualBoard)

    def test_bishop_illegal_3(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/5B2/8/PPP1PPPP/RN1QKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'f4d5', actualBoard)

    def test_bishop_illegal_4(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqk1nr/pppppp1p/8/6p1/5b2/8/PPPPP1PP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'f4h6', actualBoard)

    def test_bishop_illegal_5(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqk1nr/pppppp1p/8/6p1/5b2/8/PPPPP1PP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'f4e4', actualBoard)

    def test_move_knight_legal_1(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('b1c3', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_knight_legal_2(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3N4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('d5c3', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_knight_legal_3(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3p4/8/2N5/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('c3d5', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3N4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_knight_legal_4(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('g8h6', actualBoard)
        expectedBoard.load_from_fen("rnbqkb1r/pppppppp/7n/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_knight_legal_5(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkb1r/pppppppp/7n/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('h6f5', actualBoard)
        expectedBoard.load_from_fen("rnbqkb1r/pppppppp/8/5n2/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)


    def test_knight_illegal_1(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3N4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd5e5', actualBoard)

    def test_knight_illegal_2(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3N4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd5d4', actualBoard)

    def test_knight_illegal_3(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3N4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd5e4', actualBoard)

    def test_knight_illegal_4(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3N4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd5d3', actualBoard)

    def test_knight_illegal_5(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/3N4/8/8/PPPPPPPP/R1BQKBNR w KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd5a5', actualBoard)

    def test_knight_illegal_6(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkb1r/pppppppp/8/5n2/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'f5e5', actualBoard)

    def test_knight_illegal_7(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkb1r/pppppppp/8/5n2/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'f5g4', actualBoard)

    def test_knight_illegal_8(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("r1bqkb1r/pppppppp/8/5n2/3n4/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'f5d4', actualBoard)


    def test_move_queen_legal_1(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/8/8/8/3Q4/8/8/RNB1KBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('d4f4', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/8/8/8/5Q2/8/8/RNB1KBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_2(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/8/8/8/3Q4/8/8/RNB1KBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('d4b6', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/8/1Q6/8/8/8/8/RNB1KBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_3(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/8/1Q6/8/8/8/8/RNB1KBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('b6b3', actualBoard)
        expectedBoard.load_from_fen("rnbqkbnr/8/8/8/8/1Q6/8/RNB1KBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_4(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/8/8/8/8/1Q6/8/RNB1KBNR w KQkq - 0 1")
        actualBoard.chess_move.perform_move('b3g8', actualBoard)
        expectedBoard.load_from_fen("rnbqkbQr/8/8/8/8/8/8/RNB1KBNR w KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_5(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkb2/8/8/8/2Q4r/8/8/RNB1KBNR w KQq - 0 1")
        actualBoard.chess_move.perform_move('c4h4', actualBoard)
        expectedBoard.load_from_fen("rnbqkb2/8/8/8/7Q/8/8/RNB1KBNR w KQq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_6(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkb2/8/8/8/Q7/8/8/RNB1KBNR w KQq - 0 1")
        actualBoard.chess_move.perform_move('a4a8', actualBoard)
        expectedBoard.load_from_fen("Qnbqkb2/8/8/8/8/8/8/RNB1KBNR w KQ - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_7(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('d8h4', actualBoard)
        expectedBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/7q/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_8(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/7q/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('h4d4', actualBoard)
        expectedBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/3q4/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_9(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/3q4/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('d4d5', actualBoard)
        expectedBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/3qp3/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)

    def test_move_queen_legal_10(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/3qp3/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        actualBoard.chess_move.perform_move('d5g2', actualBoard)
        expectedBoard.load_from_fen("rnb1kbnr/pppp1ppp/8/4p3/8/8/PPPPPPqP/RNBQKBNR b KQkq - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)


    def test_queen_illegal_1(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1nbqkb2/8/8/8/3Q4/8/8/RNB1KBNR w KQ - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd4f5', actualBoard)

    def test_queen_illegal_2(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1nbqkb2/8/8/3R4/8/3Q4/8/1NB1KBNR w K - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd3d5', actualBoard)

    def test_queen_illegal_3(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1nbqkb2/8/8/3R4/8/3Q4/8/1NB1KBNR w K - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd3d6', actualBoard)

    def test_queen_illegal_4(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd8d7', actualBoard)

    def test_queen_illegal_5(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1")
        self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'd8d6', actualBoard)

    def test_evaluate_board_on_empty(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("8/8/8/8/8/8/8/8 w - - 0 1")
        self.assertEqual(0, actualBoard.evaluate_board())

    def test_is_in_check_1(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbq1bnr/ppp1pppp/4k3/8/8/8/PPP1QPPP/RNBK1BNR w KQha - 0 1")
        self.assertIsInCheck(actualBoard)

    def test_is_in_check_2(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbq1bnr/pppkpppp/8/8/8/8/PPP2PPP/RNBQKBNR w KQha - 0 1")
        self.assertIsNotInCheck(actualBoard)

    def test_is_in_check_3(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkb1r/pppnpppp/8/8/6K1/8/PPP2PPP/RNB1QBNR w HAkq - 0 1")
        self.assertIsNotInCheck(actualBoard)

    def test_is_in_check_4(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkb1r/pppnpppp/8/6K1/8/8/PPP2PPP/RNB1QBNR w HAkq - 0 1")
        self.assertIsNotInCheck(actualBoard)

    def test_is_in_check_5(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkbnr/ppp1pppp/8/5P2/6K1/8/PPP3PP/RNB1QBNR w HAkq - 0 1")
        # Test schlägt Fehl, weil der Läufer irrtümlich durch das Pferd läuft
        self.assertIsNotInCheck(actualBoard)

    def test_is_in_check_6(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqknbr/ppp1pppp/4K3/5P2/8/8/PPP3PP/RNB1QBNR w HAkq - 0 1")
        self.assertIsInCheck(actualBoard)

    def test_is_in_check_7(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbqkb1r/pppnppp1/7p/6K1/8/8/PPP2PPP/RNB1QBNR w HAkq - 0 1")
        self.assertIsInCheck(actualBoard)

    def test_is_in_check_8(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnbq1bnr/pppppppp/8/8/5P2/4k3/PPPPP1PP/RNBQKBNR b KQha - 0 1")
        self.assertIsInCheck(actualBoard)

    def test_is_check_mate_1(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/ppppqppp/5p2/8/8/5P2/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        self.assertIsInCheck(actualBoard)
        legal_moves = actualBoard.chess_move.generate_moves(actualBoard)
        self.assertFalse(actualBoard.is_check_mate(legal_moves))

    def test_is_check_mate_2(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/ppppqppp/5p2/8/8/5P2/PPPP1PPP/RNBQK1NR w KQkq - 0 1")
        self.assertIsInCheck(actualBoard)
        legal_moves = actualBoard.chess_move.generate_moves(actualBoard)
        self.assertFalse(actualBoard.is_check_mate(legal_moves))

    def test_is_check_mate_3(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/ppppqppp/5p2/8/8/5P2/PPPP1PPP/RNB1K1NR w KQkq - 0 1")
        self.assertIsInCheck(actualBoard)
        legal_moves = actualBoard.chess_move.generate_moves(actualBoard)
        self.assertFalse(actualBoard.is_check_mate(legal_moves))

    def test_is_check_mate_4(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/ppppqppp/5p2/8/8/5P2/PPPP1PPP/RNB1K2R w KQkq - 0 1")
        self.assertIsInCheck(actualBoard)
        legal_moves = actualBoard.chess_move.generate_moves(actualBoard)
        self.assertFalse(actualBoard.is_check_mate(legal_moves))

    def test_is_check_mate_5(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/ppppqppp/5p2/8/8/5P2/PPPP1PPP/RNBPKP1R w KQkq - 0 1")
        self.assertIsInCheck(actualBoard)
        legal_moves = actualBoard.chess_move.generate_moves(actualBoard)
        self.assertTrue(actualBoard.is_check_mate(legal_moves))

    def test_is_check_mate_6(self):
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("rnb1kbnr/pppp1ppp/4p3/8/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1")
        self.assertIsInCheck(actualBoard)
        legal_moves = actualBoard.chess_move.generate_moves(actualBoard)
        self.assertTrue(actualBoard.is_check_mate(legal_moves))

    def test_draw_by_repitition_1(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1kr5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
        for _ in range(3):
            actualBoard.chess_move.perform_move('g1a7', actualBoard)
            expectedBoard.load_from_fen("1kr5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('b8a8', actualBoard)
            expectedBoard.load_from_fen("k1r5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('a7g1', actualBoard)
            expectedBoard.load_from_fen("k1r5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('a8b8', actualBoard)
            expectedBoard.load_from_fen("1kr5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)
        self.assertTrue(actualBoard.chess_move.is_draw(actualBoard.chess_move.generate_moves(actualBoard), actualBoard))

    def test_draw_by_repitition_2(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1kr5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
        for _ in range(2):
            actualBoard.chess_move.perform_move('g1a7', actualBoard)
            expectedBoard.load_from_fen("1kr5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('b8a8', actualBoard)
            expectedBoard.load_from_fen("k1r5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('a7g1', actualBoard)
            expectedBoard.load_from_fen("k1r5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('a8b8', actualBoard)
            expectedBoard.load_from_fen("1kr5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)
        self.assertFalse(actualBoard.chess_move.is_draw(actualBoard.chess_move.generate_moves(actualBoard), actualBoard))

    def test_draw_by_repitition_3(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1kr5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
        for _ in range(2):
            actualBoard.chess_move.perform_move('g1a7', actualBoard)
            expectedBoard.load_from_fen("1kr5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('b8a8', actualBoard)
            expectedBoard.load_from_fen("k1r5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('a7g1', actualBoard)
            expectedBoard.load_from_fen("k1r5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('a8b8', actualBoard)
            expectedBoard.load_from_fen("1kr5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

        actualBoard.chess_move.perform_move('g1b6', actualBoard)
        expectedBoard.load_from_fen("1kr5/1b3R2/1B2p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)
        self.assertFalse(actualBoard.chess_move.is_draw(actualBoard.chess_move.generate_moves(actualBoard), actualBoard))

    def test_draw_by_repitition_4(self):
        expectedBoard = ChessBitboard()
        actualBoard = ChessBitboard()
        actualBoard.load_from_fen("1kr5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
        for _ in range(2):
            actualBoard.chess_move.perform_move('g1a7', actualBoard)
            expectedBoard.load_from_fen("1kr5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('b8a8', actualBoard)
            expectedBoard.load_from_fen("k1r5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('a7g1', actualBoard)
            expectedBoard.load_from_fen("k1r5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

            actualBoard.chess_move.perform_move('a8b8', actualBoard)
            expectedBoard.load_from_fen("1kr5/1b3R2/4p3/4Pn1p/8/2P3p1/1KP4r/6B1 w - - 0 1")
            self.assertEqualBitboards(expectedBoard, actualBoard)

        actualBoard.chess_move.perform_move('g1a7', actualBoard)
        expectedBoard.load_from_fen("1kr5/Bb3R2/4p3/4Pn1p/8/2P3p1/1KP4r/8 w - - 0 1")
        self.assertEqualBitboards(expectedBoard, actualBoard)
        self.assertTrue(actualBoard.chess_move.is_draw(actualBoard.chess_move.generate_moves(actualBoard), actualBoard))

    # def test_en_passant(self):
    #     actualBoard.load_from_fen("4k3/8/8/4pP2/8/8/8/4K3 w - e6 0 2")
    #     actualBoard.chess_move.perform_move('f5e6', actualBoard)
    #     expectedBoard.load_from_fen("4k3/8/4P3/8/8/8/8/4K3 b - - 0 2")
    #     self.assertEqualBitboards(expectedBoard, actualBoard)
    #
    # def test_en_pessant_illegal_1(self):
    #     expectedBoard = ChessBitboard()
    #     actualBoard = ChessBitboard()
    #     actualBoard.load_from_fen("4k3/8/8/3pP3/8/8/8/4K3 w - - 0 2")
    #     self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'e5d6', actualBoard)
    #
    # def test_en_pessant_illegal_2(self):
    #     expectedBoard = ChessBitboard()
    #     actualBoard = ChessBitboard()
    #     actualBoard.load_from_fen("4k3/8/5P2/4p3/8/8/8/4K3 w - e6 0 2")
    #     self.assertRaises(IllegalMoveException, actualBoard.chess_move.perform_move, 'f6e6', actualBoard)


if __name__ == '__main__':
    unittest.main()
