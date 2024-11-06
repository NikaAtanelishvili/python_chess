from board import Board

def main():
    board = Board()
    board.print_board()

    while True:
        print(f"{board.turn.capitalize()}'s turn.")

        # Get player input
        start = input("Enter the position of the piece to move (e.g., 'e2'): ")
        if len(start) != 2 or not start[0].isalpha() or not start[1].isdigit():
            print("Invalid input. Please enter a valid position (e.g., 'e2').")
            continue

        end = input("Enter the target position (e.g., 'e4'): ")
        if len(end) != 2 or not end[0].isalpha() or not end[1].isdigit():
            print("Invalid input. Please enter a valid position (e.g., 'e4').")
            continue

        # Move the piece
        board.move_piece(start, end)
        board.print_board()

if __name__ == "__main__":
    main()

