from chessBitboard import ChessBitboard

if __name__ == "__main__":
    chessBitboard = ChessBitboard()


    # #Set initial positions for white pieces using binary literals
    # bitboards[WHITE] =  int("0b0000100000000000000000000000000000000000001000000010000000000101", 2)
    # bitboards[KING] =   int("0b0000100000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[PAWN] =   int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[KNIGHT] = int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[BISHOP] = int("0b0000000000000000000000000000000000000000001000000000000000000101", 2)
    # bitboards[ROOK] =   int("0b0000000000000000000000000000000000000000000000000010000000000000", 2)
    # bitboards[QUEEN] =  int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)

    # # Set initial positions for black pieces using binary literals
    # bitboards[BLACK] =   int("0b0000000000000001000000000000000001000000000000000000100000000000", 2)
    # bitboards[KNIGHT] |= int("0b0000000000000001000000000000000001000000000000000000100000000000", 2)
    # bitboards[PAWN] |=   int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[BISHOP] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[ROOK] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[QUEEN] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # bitboards[KING] |= int("0b0000000000000000000000000000000000000000000000000000000000000000", 2)
    # print_board(bitboards)

    # chessBitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2")
    # chessBitboard.perform_move("e2e4")
    # chessBitboard.print_bitboards()
    # chessBitboard.print_board()
    # chessBitboard.print_legal_moves(chessBitboard.bitboards, chessBitboard.current_player)
    chessBitboard.load_from_fen("rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1")
    # chessBitboard.print_board()
    chessBitboard.print_bitboards()