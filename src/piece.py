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


class King(Piece):
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

        # Check if the move is exactly one square away in any direction
        row_diff = abs(end_row_pos - start_row_pos)
        col_diff = abs(end_col_pos - start_col_pos)

        return max(row_diff, col_diff) == 1


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
            target_piece = board[end_row_pos][end_col_pos]

            # Make sure the target square is not empty and has an enemy piece
            return target_piece != " " and target_piece.islower() != board[start_row_pos][start_col_pos].islower()

        return False


class Rook(Piece):
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

        if start_row_pos != end_row_pos and start_col_pos != end_col_pos:
            return False

        # Horizontal
        if start_row_pos == end_row_pos and start_col_pos != end_col_pos:
            # [2][0] ->/<- [2][5]
            step = 1 if end_col_pos > start_col_pos else -1
            for col in range(start_col_pos + step, end_col_pos, step):
                if board[start_row_pos][col] != ' ': return False

        # Vertical
        if start_row_pos != end_row_pos and start_col_pos == end_col_pos:
            # [0][0] ->/<- [5][0]
            step = 1 if end_row_pos > start_row_pos else -1
            for row in range(start_row_pos + step, end_row_pos, step):
                if board[row][start_col_pos] != ' ': return False

        # Destination is empty or occupied by the enemy team
        target_piece = board[end_row_pos][end_col_pos]

        if target_piece != " " or target_piece.islower() != board[start_row_pos][start_col_pos].islower():
            return False

        return True


class Bishop(Piece):
    def is_valid_move(self, start, end, board):
        start_row_pos, start_col_pos = _pos_to_cords(start)
        end_row_pos, end_col_pos = _pos_to_cords(end)

        # Move must be diagonal
        if abs(end_row_pos - start_row_pos) != abs(end_col_pos - start_col_pos):
            return False

        # Check if path is clear
        row_step = 1 if end_row_pos > start_row_pos else -1
        col_step = 1 if end_col_pos > start_col_pos else -1

        row, col = start_row_pos + row_step, start_col_pos + col_step
        while row < end_row_pos and col < end_col_pos:
            if board[row][col] != ' ': return False
            row += row_step
            col += col_step

        # Destination is empty or occupied by the enemy team
        target_piece = board[end_row_pos][end_col_pos]
        if target_piece != " " or target_piece.islower() != board[row][col].islower():
            return False

        return True
