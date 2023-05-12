import unittest
from ChessBitboard import ChessBitboard

class TestChessBitboard(unittest.TestCase):

    def setUp(self):
        self.testboard = ChessBitboard()
        self.bitboard = ChessBitboard()

    def test_initial_board(self):
        self.bitboard.initialize_bitboards()
        self.testboard.fen_to_bitboards("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(self.bitboard.bitboards, self.testboard.bitboards)

    def test_move_pawn(self):
        self.bitboard.perform_move('e2e4')
        self.testboard.fen_to_bitboards("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")
        self.assertEqual(self.bitboard.bitboards, self.testboard.bitboards)

if __name__ == '__main__':
    unittest.main()
