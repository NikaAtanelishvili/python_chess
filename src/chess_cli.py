from board import Board

def main():
    board = Board()
    board.print_board()

    draw_offered = False

    print("---Type 'resign' to concede---")
    print("---Type 'draw' to offer a draw---")

    while True:
        print(f"{board.turn.capitalize()}'s turn.")

        # Check if a draw has been offered
        if draw_offered:
            response = input("A draw has been offered. Type 'accept' to accept or 'reject' to continue: ").lower()
            if response == "accept":
                print("The game ends in a draw!")
                break
            elif response == "reject":
                print("Draw offer rejected. Game continues.")
                draw_offered = False

        # Get player input
        start = input("Enter the position of the piece to move (e.g., 'e2'):")

        if start.lower() == 'resign':
            print(f"{'White' if board.turn == 'black' else 'Black'} wins by resignation!")
            break

        if start.lower() == 'draw':
            draw_offered = True
            continue

        if len(start) != 2 or not start[0].isalpha() or not start[1].isdigit():
            print("Invalid input. Please enter a valid position (e.g., 'e2').")
            continue

        end = input("Enter the target position (e.g., 'e4'): ")

        if end.lower() == 'resign':
            print(f"{'White' if board.turn == 'black' else 'Black'} wins by resignation!")
            break

        if end.lower() == 'draw':
            draw_offered = True
            continue

        if len(end) != 2 or not end[0].isalpha() or not end[1].isdigit():
            print("Invalid input. Please enter a valid position (e.g., 'e4').")
            continue

        # Move the piece
        board.move_piece(start, end)
        board.print_board()

if __name__ == "__main__":
    main()

