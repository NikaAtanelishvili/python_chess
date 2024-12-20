from typing import List, Union, Optional

import pygame
from pygame.examples.midi import NullKey

from piece import *


def scale_image(image, square_size, margin=5):
    # Calculate effective size by subtracting the margin
    effective_size = square_size - 2 * margin

    # Get original image dimensions
    original_width, original_height = image.get_size()

    # Determine scaling factor to fit the image within the effective size
    scaling_factor = min(effective_size / original_width, effective_size / original_height)

    # Calculate new dimensions
    new_width = int(original_width * scaling_factor)
    new_height = int(original_height * scaling_factor)

    # Scale the image
    return pygame.transform.scale(image, (new_width, new_height)), margin


class Board:
    def __init__(self):
        # Use Union to specify that each board cell can contain a string or a piece
        self.board: List[List[Optional[Union[str, Rook, Knight, Bishop, Queen, King, Pawn]]]] = [
            [' ' for _ in range(8)] for _ in range(8)
        ]
        self.setup_pieces()
        self.turn = 'white'
        self.en_passant_target = None  # Square available for en passant capture
        self.square_size = 100
        self.colors = [(240, 217, 181), (181, 136, 99)]
        self.selected_piece = None
        self.highlighted_moves = []

        # For blinking animation when king is checked
        self.king_in_check = False
        self.king_in_check_position = None
        self.check_start_time = None

        # Popup state for checkmate popup
        self.running = True
        self.draw_popup = False
        self.resign_popup = False
        self.checkmate_popup = False
        self.popup_message = ""
        self.game_over = False

        # Popup start for promoting
        self.promotion_popup = False
        self.promotion_position = None
        self.promotion_piece = None


    def setup_pieces(self):
        self.board[0] = [
            ' ', Knight('black', 'b8'), Bishop('black', 'c8'),
            Queen('black', 'd8'), King('black', 'e8'),
            Bishop('black', 'f8'), Knight('black', 'g8'), Rook('black', 'h8')
        ]
        self.board[1] = [Pawn('black', f'{chr(97 + col)}7') for col in range(8)]

        # White pieces
        self.board[6] = [Pawn('white', f'{chr(97 + col)}2') for col in range(8)]
        self.board[7] = [
            Rook('white', 'a1'), ' ', ' ',
            ' ', King('white', 'e1'),
            ' ', ' ', Rook('white', 'h1')
        ]

    def draw_board(self, screen):
        for row in range(8):
            for col in range(8):
                pos = cords_to_pos(row, col)

                # Alter square colors
                color = self.colors[(row + col) % 2]

                # Blinking animation
                if pos == self.king_in_check_position and self.king_in_check:
                    elapsed_time = pygame.time.get_ticks() - self.check_start_time
                    if elapsed_time < 500:  # Blink for 500ms
                        color = (255, 0, 0)  # Red
                    else:
                        # Stop blinking after 500ms
                        self.king_in_check = False
                        self.king_in_check_position = None

                pygame.draw.rect(
                    screen,
                    color,
                    (col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                )

                # Highlight moves
                if cords_to_pos(row, col) in self.highlighted_moves:
                    pygame.draw.rect(
                        screen,
                        (255, 255, 0),  # Yellow border
                        (col * self.square_size, row * self.square_size, self.square_size, self.square_size),
                        5  # Border thickness
                    )

                piece = self.board[row][col]
                if piece != " ":
                    self.draw_piece(screen, piece, col, row)

    def handle_click(self, mouse_x, mouse_y):
        col = mouse_x // self.square_size
        row = mouse_y // self.square_size

        if 0 <= row < 8 and 0 <= col < 8:  # Ensure click is within bounds
            clicked_piece = self.board[row][col]

            # If a piece is clicked
            if clicked_piece != " " and clicked_piece.color == self.turn:
                self.selected_piece = clicked_piece
                self.highlighted_moves = self.get_all_possible_moves(clicked_piece)

            # If clicking on an empty square or deselecting
            elif self.selected_piece and cords_to_pos(row, col) in self.highlighted_moves:
                self.move_piece(self.selected_piece.position, cords_to_pos(row, col))
                self.selected_piece = None
                self.highlighted_moves = []

            else:
                # Clear selection
                self.selected_piece = None
                self.highlighted_moves = []

    def draw_piece(self, screen, piece, col, row):
        # Scale the image with margin
        image, margin = scale_image(piece.image, self.square_size, margin=10)

        # Calculate the position to center the image within the square
        x = col * self.square_size + (self.square_size - image.get_width()) // 2
        y = row * self.square_size + (self.square_size - image.get_height()) // 2

        # Blit the image on the screen
        screen.blit(image, (x, y))

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
        print('checkmate fun is running')
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
        print(piece, possible_moves)
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
            # Handle castling - Put the Rook in place after castling
            if isinstance(piece, King) and abs(start_col - end_col) == 2:  # Castling move
                rook_start_col = 0 if end_col < start_col else 7
                rook_end_col = 3 if end_col < start_col else 5  # New rook position after castling

                rook = self.board[start_row][rook_start_col]
                if not isinstance(rook, Rook):
                    raise ValueError("Invalid rook position for castling.")

                # Move the rook
                self.board[start_row][rook_end_col] = rook
                self.board[start_row][rook_start_col] = ' '
                rook.position = cords_to_pos(start_row, rook_end_col)
                rook.has_moved = True

                # Mark the king as moved
                piece.has_moved = True

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

            # Move piece
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = ' '
            piece.position = end

            # Handle promotion
            if isinstance(piece, Pawn) and piece.is_promotion_square(end_row):
                self.promotion_popup = True
                self.promotion_position = (end_row, end_col)
                self.promotion_piece = piece

            # Check if king is in check after the move
            if self.is_in_check(self.turn):
                # Revert move
                self.board[start_row][start_col] = piece
                self.board[end_row][end_col] = captured_piece
                piece.position = start

                # Set check state and start time
                self.king_in_check = True
                self.king_in_check_position = self.find_king(self.turn)
                self.check_start_time = pygame.time.get_ticks()

                print("Invalid move: your King would be in check.")
            # Check for checkmate after the opponent's move
            else:
                move_sound = pygame.mixer.Sound(
                    './assets/sound_effects/move-self.mp3')  # Replace with your sound file path

                piece.has_moved = True
                piece.position = end

                # Set check state and start time
                self.king_in_check = False
                self.king_in_check_position = None
                self.check_start_time = None

                opponent_color = 'black' if self.turn == 'white' else 'white'
                if self.is_in_checkmate(opponent_color):
                    print(f"Checkmate! {self.turn.capitalize()} wins!")

                    self.game_over = True
                    self.popup_message = f"Checkmate! {self.turn.capitalize()} wins!"
                    self.draw_popup = True  # Use draw_popup to display the end-game popup
                    self.resign_popup = True
                move_sound.play()
                self.switch_turn()
        else:
            print("Invalid move: either it's not your turn or the move is invalid.")


    def promote_pawn_to(self, piece_type):
        """Finalize the pawn promotion based on the player's choice."""
        row, col = self.promotion_position
        color = self.promotion_piece.color
        position = self.promotion_piece.position

        # Create the new piece
        if piece_type == "Q":
            self.board[row][col] = Queen(color, position)
        elif piece_type == "R":
            self.board[row][col] = Rook(color, position)
        elif piece_type == "B":
            self.board[row][col] = Bishop(color, position)
        elif piece_type == "N":
            self.board[row][col] = Knight(color, position)
        else:
            self.board[row][col] = Queen(color, position)  # Default to Queen

        # Reset promotion state
        self.promotion_popup = False
        self.promotion_position = None
        self.promotion_piece = None


    def switch_turn(self):
        # Toggle turn between white and black
        self.turn = "black" if self.turn == "white" else "white"



