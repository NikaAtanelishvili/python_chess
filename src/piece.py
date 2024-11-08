class Piece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # Example: 'e2'
        self.has_moved = False

    def is_valid_move(self, start, end, board, game):
        """Validate if the move is allowed (to be overridden by subclasses)."""
        raise NotImplementedError("This method should be overridden in subclasses.")

def pos_to_cords(position):
    """Converts piece's position "e2, a3" to coords(indexes)"""
    col = ord(position[0]) - ord('a')
    row = 8 - int(position[1])

    return row, col

def cords_to_pos(row, col):
    return f"{chr(col + ord('a'))}{8 - row}"

'''Destination is empty or occupied by the enemy team'''
def _is_valid_destination(board, row, col, moving_piece_color):
    target_piece = board[row][col]

    if target_piece != ' ' and hasattr(target_piece, 'color'):
        if target_piece.color == moving_piece_color:
            # Cannot capture own piece
            return False  # Own piece at destination
    # Destination is either empty or contains an opponent's piece
    return True

def _is_vertical_path_clear(board, start_row_pos, end_row_pos, col):
    step = 1 if end_row_pos > start_row_pos else -1

    for row in range(start_row_pos + step, end_row_pos, step):
        if board[row][col] != ' ': return False  # Path is blocked

    return _is_valid_destination(board, end_row_pos, col, board[start_row_pos][col].color)

def _is_horizontal_path_clear(board, row, start_col_pos, end_col_pos):
    step = 1 if end_col_pos > start_col_pos else -1

    for col in range(start_col_pos + step, end_col_pos, step):
        if board[row][col] != ' ': return False

    return _is_valid_destination(board, row, end_col_pos, board[row][start_col_pos].color)

def _is_diagonal_path_clear(board, start_row_pos, start_col_pos, end_row_pos, end_col_pos):
    row_step = 1 if end_row_pos > start_row_pos else -1
    col_step = 1 if end_col_pos > start_col_pos else -1

    row, col = start_row_pos + row_step, start_col_pos + col_step
    while row != end_row_pos and col != end_col_pos:
        if board[row][col] != ' ':
            return False  # Path is blocked
        row += row_step
        col += col_step

    return _is_valid_destination(board, end_row_pos, end_col_pos, board[start_row_pos][start_col_pos].color)


class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = "♚" if color == "black" else "♔"

    def is_valid_move(self, start, end, board, game):
        start_row_pos, start_col_pos = pos_to_cords(start)
        end_row_pos, end_col_pos = pos_to_cords(end)

        # Check if the move is exactly one square away in any direction
        row_diff = abs(end_row_pos - start_row_pos)
        col_diff = abs(end_col_pos - start_col_pos)

        # Castling logic
        if abs(start_col_pos - end_col_pos) == 2:  # King moves 2 squares sideways
            return self.can_castle(start, end, board, game)

        if max(row_diff, col_diff) == 1:
            # Temporarily move the King to the destination
            original_piece = board[end_row_pos][end_col_pos]
            board[end_row_pos][end_col_pos] = self
            board[start_row_pos][start_col_pos] = " "
            self.position = end

            # Check if the King is in check after the move
            in_check = game.is_in_check(self.color)

            # Revert the move
            board[start_row_pos][start_col_pos] = self
            board[end_row_pos][end_col_pos] = original_piece
            self.position = start

            if in_check:
                return False
            else:
                return _is_valid_destination(board, end_row_pos, end_col_pos, board[start_row_pos][start_col_pos].color)
        else:
            return False

    def can_castle(self, start, end, board, game):
        if self.has_moved:
            print('King was moved before, you can no longer castle')
            return False

        # Define rook's start position based on color and side (king or queen side)
        row, col = pos_to_cords(start) # E.G. 7 4
        rook_col = 7 if end[1] < start[1] else 0  # Queen-side or king-side castling

        rook = board[row][rook_col]
        if not isinstance(rook, Rook) or rook.has_moved:
            print('Castling failed, Rook was moved or is absent!')
            return False

        # # Check squares between king and rook are empty
        step = 1 if rook_col == 0 else -1

        # Use _is_horizontal_path_clear to check if the path between king and rook is clear
        if not _is_horizontal_path_clear(board, row, col, rook_col + step):
            print(row, col, rook_col + step)
            return False

        # Ensure no squares king crosses or lands on are under attack
        temp_positions = [start, cords_to_pos(row, col + step), end]
        opponent_color = 'black' if self.color == 'white' else 'white'

        for pos in temp_positions:
            for row in game.board:
                for piece in row:
                    if piece != ' ' and piece.color == opponent_color:
                        if piece.is_valid_move(piece.position, pos, game.board, game):
                            return False

        return True


class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = "♟" if color == "black" else "♙"
        self.just_moved_two_squares = False  # Track if this pawn just moved two squares (for en ...)

    def is_valid_move(self, start, end, board, game):
        start_row_pos, start_col_pos = pos_to_cords(start)
        end_row_pos, end_col_pos = pos_to_cords(end)

        direction = -1 if self.color == 'white' else 1  # White moves up (-1), Black moves down (+1)

        # Reset the two-square move tracker unless this move is a two-square move
        self.just_moved_two_squares = False

        # Regular move (forward one square)
        if start_col_pos == end_col_pos and end_row_pos == start_row_pos + direction:
            return board[end_row_pos][end_col_pos] == ' '  # Must be an empty spot

        # Initial move (forward two squares)
        if start_col_pos == end_col_pos:
            if (self.color == 'white' and start_row_pos == 6) or (self.color == 'black' and start_row_pos == 1):
                if end_row_pos == start_row_pos + 2 * direction:
                    if board[start_row_pos + direction][start_col_pos] == ' ' and board[end_row_pos][end_col_pos] == ' ':
                        self.just_moved_two_squares = True
                        return True  # Both squares must be empty

        # Capture (diagonal move)
        if abs(start_col_pos - end_col_pos) == 1 and end_row_pos == start_row_pos + direction:
            target_piece = board[end_row_pos][end_col_pos]
            if target_piece != ' ' and hasattr(target_piece, 'color'):
                if target_piece.color != self.color:
                    return True  # Can capture opponent's piece
            # En passant capture
            if game.en_passant_target == end and isinstance(board[start_row_pos][end_col_pos], Pawn):
                if board[start_row_pos][end_col_pos].color != self.color:
                    return True  # Valid en passant capture

        return False  # Move is invalid


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = "♜" if color == "black" else "♖"

    def is_valid_move(self, start, end, board, game):
        start_row_pos, start_col_pos = pos_to_cords(start)
        end_row_pos, end_col_pos = pos_to_cords(end)

        if start_row_pos != end_row_pos and start_col_pos != end_col_pos:
            return False

        # Horizontal
        if start_row_pos == end_row_pos:
            return _is_horizontal_path_clear(board, start_row_pos, start_col_pos, end_col_pos)

        # Vertical
        if start_col_pos == end_col_pos:
            return _is_vertical_path_clear(board, start_row_pos, end_row_pos, start_col_pos)

        return False


class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = "♝" if color == "black" else "♗"

    def is_valid_move(self, start, end, board, game):
        start_row_pos, start_col_pos = pos_to_cords(start)
        end_row_pos, end_col_pos = pos_to_cords(end)

        # Move must be diagonal
        if abs(end_row_pos - start_row_pos) != abs(end_col_pos - start_col_pos):
            return False

        # Check if path is clear
        return _is_diagonal_path_clear(board, start_row_pos, start_col_pos, end_row_pos, end_col_pos)


class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = "♛" if color == "black" else "♕"

    def is_valid_move(self, start, end, board, game):
        start_row_pos, start_col_pos = pos_to_cords(start)
        end_row_pos, end_col_pos = pos_to_cords(end)

        '''Determine if move is diagonal, horizontal or vertical'''
        # Diagonal
        if abs(end_row_pos - start_row_pos) == abs(end_col_pos - start_col_pos):
            return _is_diagonal_path_clear(board, start_row_pos, start_col_pos, end_row_pos, end_col_pos)

        # Horizontal
        if start_row_pos == end_row_pos and start_col_pos != end_col_pos:
            return _is_horizontal_path_clear(board, start_row_pos, start_col_pos, end_col_pos)

        # Vertical
        if start_row_pos != end_row_pos and start_col_pos == end_col_pos:
            return _is_vertical_path_clear(board, start_row_pos, end_row_pos, start_col_pos)

        return False


class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.symbol = "♞" if color == "black" else "♘"

    def is_valid_move(self, start, end, board, game):
        start_row_pos, start_col_pos = pos_to_cords(start)
        end_row_pos, end_col_pos = pos_to_cords(end)

        # Calculate row and column differences
        row_diff = abs(end_row_pos - start_row_pos)
        col_diff = abs(end_col_pos - start_col_pos)

        # Check for L-shape movement (2 squares in one direction, 1 in the other)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return _is_valid_destination(board, end_row_pos, end_col_pos, board[start_row_pos][start_col_pos].color)

        return False



