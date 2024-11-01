from typing import List, Union, Optional

from piece import *

class Board:
    def __init__(self):
        # Use Union to specify that each board cell can contain a string or a piece
        self.board: List[List[Optional[Union[str, Rook, Knight, Bishop, Queen, King, Pawn]]]] = [
            [' ' for _ in range(8)] for _ in range(8)
        ]
        self.setup_pieces()

    def setup_pieces(self):
        self.board[0] = [
            Rook('black', 'a8'), Knight('black', 'b8'), Bishop('black', 'c8'),
            Queen('black', 'd8'), King('black', 'e8'),
            Bishop('black', 'f8'), Knight('black', 'g8'), Rook('black', 'h8')
        ]
        self.board[1] = [Pawn('black', f'{chr(97 + col)}7') for col in range(8)]

        # White pieces
        self.board[6] = [Pawn('white', f'{chr(97 + col)}2') for col in range(8)]
        self.board[7] = [
            Rook('white', 'a1'), Knight('white', 'b1'), Bishop('white', 'c1'),
            Queen('white', 'd1'), King('white', 'e1'),
            Bishop('white', 'f1'), Knight('white', 'g1'), Rook('white', 'h1')
        ]

    def print_board(self):
        """Display the board with piece symbols."""
        for row in self.board:
            print(' '.join(piece.symbol if piece != " " and hasattr(piece, 'symbol') else " " for piece in row))
        print()

    def move_piece(self, start, end):
        """Move a piece from start to end if the move is valid."""
        start_row, start_col = pos_to_cords(start)
        end_row, end_col = pos_to_cords(end)

        piece = self.board[start_row][start_col]

        # Check if there's a piece at the start position and if the move is valid
        if piece != " " and hasattr(piece, 'is_valid_move') and piece.is_valid_move(start, end, self.board):
            self.board[end_row][end_col] = piece  # Move piece to the new position
            piece.position = end
            self.board[start_row][start_col] = " "  # Clear the old position
        else:
            print("Invalid move")


