import unittest
from ChessBitboard import ChessBitboard

class TestChessBitboard(unittest.TestCase):

    def setUp(self):
        self.testboard = ChessBitboard()
        self.bitboard = ChessBitboard()

    def test_initial_board(self):
        self.bitboard.initialize_bitboards()
        self.testboard.load_from_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(self.bitboard.bitboards, self.testboard.bitboards)

    def test_move_pawn_legal_1(self):
        self.bitboard.perform_move('e2e4')
        self.testboard.load_from_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(self.bitboard.bitboards, self.testboard.bitboards)
    def test_move_pawn_illegal_1(self):
        self.assertRaises(Exception, self.bitboard.perform_move, 'e7e5')

if __name__ == '__main__':
    unittest.main()
