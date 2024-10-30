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
