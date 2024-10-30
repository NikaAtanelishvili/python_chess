class Board:
    def __init__(self):
        self.board = [[" " for _ in range(8)] for _ in range(8)]
        self.setup_pieces()


    def setup_pieces(self):
        self.board[0] = [
            "R", "N", "B", "Q", "K", "B", "N", "R"
        ]  # Black pieces
        self.board[1] = ["P"] * 8  # Black pawns
        self.board[6] = ['p'] * 8 # Write pawns
        self.board[7] = [
            "r", "n", "b", "q", "k", "b", "n", "r"
        ] # White pieces


    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print()



