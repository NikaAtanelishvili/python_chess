from board import Board

def main():
    board = Board()
    board.print_board()

    while True:
        print(f"{board.turn.capitalize()}'s turn.")

        # Get player input
        start = input("Enter the position of the piece to move (e.g., 'e2'): ")
        end = input("Enter the target position (e.g., 'e4'): ")

        # Move the piece
        board.move_piece(start, end)
        board.print_board()

if __name__ == "__main__":
    main()

