class Piece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # Example: 'e2'

    def is_valid_move(self, start, end, board):
        """Validate if the move is allowed (to be overridden by subclasses)."""
        raise NotImplementedError("This method should be overridden in subclasses.")


def _pos_to_cords(position):
    """Converts piece's position "e2, a3" to coords(indexes)"""
    col = ord(position[0]) - ord('a')
    row = 8 - int(position[1])

    return row, col


'''Destination is empty or occupied by the enemy team'''
def _is_valid_destination(board, row, col):
    target_piece = board[row][col]
    if target_piece != " " or target_piece.islower() != board[row][col].islower():
        return False

    return True

def _is_vertical_path_clear(board, start_row_pos, end_row_pos, col):
    step = 1 if end_row_pos > start_row_pos else -1
    for row in range(start_row_pos + step, end_row_pos, step):
        if board[row][col] != ' ': return False

    return _is_valid_destination(board, end_row_pos, col)


def _is_horizontal_path_clear(board, row, start_col_pos, end_col_pos):
    step = 1 if end_col_pos > start_col_pos else -1
    for col in range(start_col_pos + step, end_col_pos, step):
        if board[row][col] != ' ': return False

    return _is_valid_destination(board, row, end_col_pos)


def _is_diagonal_path_clear(board, start_row_pos, start_col_pos, end_row_pos, end_col_pos):
    # Check if path is clear
    row_step = 1 if end_row_pos > start_row_pos else -1
    col_step = 1 if end_col_pos > start_col_pos else -1

    row, col = start_row_pos + row_step, start_col_pos + col_step
    while row < end_row_pos and col < end_col_pos:
        if board[row][col] != ' ': return False
        row += row_step
        col += col_step

    return _is_valid_destination(board, end_row_pos, end_col_pos)


class King(Piece):
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

        # Check if the move is exactly one square away in any direction
        row_diff = abs(end_row_pos - start_row_pos)
        col_diff = abs(end_col_pos - start_col_pos)

        if max(row_diff, col_diff) == 1:
            return _is_valid_destination(board, end_row_pos, end_col_pos)

        return False


class Pawn(Piece):
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

        direction = 1 if board[start_row_pos][start_col_pos].isupper() else -1

        # Regular move
        if start_col_pos == end_col_pos and end_row_pos == start_row_pos - direction:
            return board[end_row_pos][end_col_pos] == ' ' # Must be empty spot

        # Initial move (2 squares)
        if start_col_pos == end_col_pos and start_row_pos in (1, 6) and end_row_pos - start_row_pos == 2 * direction:
            return board[start_row_pos + direction][start_col_pos] == ' ' and board[end_row_pos][end_col_pos] == ' ' # Must be empty spot

        # Capture ( Diagonal )
        if abs(start_col_pos - end_col_pos) == 1 and end_row_pos == start_row_pos - direction:
            return _is_valid_destination(board, end_row_pos, end_col_pos)

        return False


class Rook(Piece):
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

        if start_row_pos != end_row_pos and start_col_pos != end_col_pos:
            return False

        # Horizontal
        if start_row_pos == end_row_pos and start_col_pos != end_col_pos:
            return _is_horizontal_path_clear(board, start_row_pos, start_col_pos, end_col_pos)

        # Vertical
        if start_row_pos != end_row_pos and start_col_pos == end_col_pos:
            return _is_vertical_path_clear(board, start_row_pos, end_row_pos, start_col_pos)

        return False



class Bishop(Piece):
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

        # Move must be diagonal
        if abs(end_row_pos - start_row_pos) != abs(end_col_pos - start_col_pos):
            return False

        # Check if path is clear
        return _is_diagonal_path_clear(board, start_row_pos, start_col_pos, end_row_pos, end_col_pos)


class Queen(Piece):
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

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
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

        # Calculate row and column differences
        row_diff = abs(end_row_pos - start_row_pos)
        col_diff = abs(end_col_pos - start_col_pos)

        # Check for L-shape movement (2 squares in one direction, 1 in the other)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return _is_valid_destination(board, end_row_pos, end_col_pos)



