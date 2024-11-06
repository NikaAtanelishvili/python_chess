from typing import List, Union, Optional

from piece import *

class Board:
    def __init__(self):
        # Use Union to specify that each board cell can contain a string or a piece
        self.board: List[List[Optional[Union[str, Rook, Knight, Bishop, Queen, King, Pawn]]]] = [
            [' ' for _ in range(8)] for _ in range(8)
        ]
        self.setup_pieces()
        self.turn = 'white'
        self.en_passant_target = None  # Square available for en passant capture

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

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        opponent_color = 'black' if color == 'white' else 'white'

        for row in self.board:
            for piece in row:
                if piece != ' ' and piece.color == opponent_color:
                    if piece.is_valid_move(piece.position, king_pos, self.board, self):
                        return True

        return False

    def is_in_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in self.board:
            for piece in row:
                if piece != ' ' and piece.color == color:
                    possible_moves = self.get_all_possible_moves(piece)
                    for move in possible_moves:
                        # Simulate move
                        start_pos = piece.position
                        end_pos = move
                        start_row, start_col = pos_to_cords(start_pos)
                        end_row, end_col = pos_to_cords(end_pos)
                        captured_piece = self.board[end_row][end_col]

                        self.board[end_row][end_col] = piece
                        self.board[start_row][start_col] = ' '
                        piece.position = end_pos

                        if not self.is_in_check(color):
                            # Revert move
                            self.board[start_row][start_col] = piece
                            self.board[end_row][end_col] = captured_piece
                            piece.position = start_pos
                            return False

                        # Revert move
                        self.board[start_row][start_col] = piece
                        self.board[end_row][end_col] = captured_piece
                        piece.position = start_pos
        return True # No valid moves were found, It's checkmate

    def get_all_possible_moves(self, piece):
        possible_moves = []
        for row in range(8):
            for col in range(8):
                end_pos = cords_to_pos(row, col)
                if piece.is_valid_move(piece.position, end_pos, self.board, self):
                    possible_moves.append(end_pos)

        return possible_moves


    def find_king(self, color):
        for row in self.board:
            for piece in row:
                if piece != ' ' and isinstance(piece, King) and piece.color == color:
                    return piece.position

        return None

    def move_piece(self, start, end):
        """Move a piece from start to end if the move is valid."""
        start_row, start_col = pos_to_cords(start)
        end_row, end_col = pos_to_cords(end)

        piece = self.board[start_row][start_col]

        # Check if there's a piece at the start position and if the move is valid
        if piece != " " and piece.color == self.turn and hasattr(piece, 'is_valid_move') and piece.is_valid_move(start, end, self.board, self):
            # Handle en passant
            if isinstance(piece, Pawn) and abs(start_row - end_row) == 2:
                # Set en passant target if pawn moves two squares
                self.en_passant_target = cords_to_pos((start_row + end_row) // 2, start_col)

            # En passant capture handling
            if isinstance(piece, Pawn) and end == self.en_passant_target:
                capture_row, capture_col = start_row, end_col
                captured_piece = self.board[capture_row][capture_col]
                self.board[capture_row][capture_col] = ' '  # Remove the captured pawn
            else:
                captured_piece = self.board[end_row][end_col]

            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = ' '
            piece.position = end

            # Check if king is in check after the move
            if self.is_in_check(self.turn):
                # Revert move
                self.board[start_row][start_col] = piece
                self.board[end_row][end_col] = captured_piece
                piece.position = start
                print("Invalid move: your King would be in check.")
            # Check for checkmate after the opponent's move
            else:
                opponent_color = 'black' if self.turn == 'white' else 'white'
                if self.is_in_checkmate(opponent_color):
                    print(f"Checkmate! {self.turn.capitalize()} wins!")
                    exit()
                self.switch_turn()
        else:
            print("Invalid move: either it's not your turn or the move is invalid.")

    def switch_turn(self):
        # Toggle turn between white and black
        self.turn = "black" if self.turn == "white" else "white"



