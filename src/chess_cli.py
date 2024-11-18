import pygame

from board import Board

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 900))
    pygame.display.set_caption('Chess Game')

    board = Board()

    # Fonts
    font = pygame.font.Font(None, 36)  # Font for text
    button_font = pygame.font.Font(None, 28)  # Font for buttons

    running = True
    draw_popup = False  # Tracks whether the draw popup is active

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if draw_popup:
                    # Handle draw popup buttons
                    if 290 <= mouse_x <= 390 and 400 <= mouse_y <= 440:  # Accept button
                        print("Draw accepted!")
                        running = False  # End game
                    elif 410 <= mouse_x <= 510 and 400 <= mouse_y <= 440:  # Reject button
                        print("Draw rejected!")
                        draw_popup = False  # Close popup
                else:
                    # Handle main buttons
                    if 650 <= mouse_x <= 780 and 815 <= mouse_y <= 845:  # Resign button
                        print(f"{board.turn} player resigned!")
                        running = False  # End game
                    elif 650 <= mouse_x <= 780 and 855 <= mouse_y <= 885:  # Draw button
                        print("Draw offer made!")
                        draw_popup = True  # Show draw popup

                if mouse_y <= 800:  # Ensure the click is on the board, not the UI
                    board.handle_click(mouse_x, mouse_y)

        screen.fill((0, 0, 0))
        board.draw_board(screen)

        # Draw current player's turn
        turn_text = font.render(f"Turn: {board.turn.capitalize()}", True, (255, 255, 255))
        screen.blit(turn_text, (30, 832))  # Position just below the board

        # Draw buttons
        pygame.draw.rect(screen, (200, 0, 0), (650, 815, 130, 30))  # Resign button
        pygame.draw.rect(screen, (0, 200, 0), (650, 855, 130, 30))  # Draw button

        # Add button text
        resign_text = button_font.render("Resign", True, (255, 255, 255))
        draw_text = button_font.render("Draw", True, (255, 255, 255))
        screen.blit(resign_text, (660, 820))
        screen.blit(draw_text, (660, 860))

        # Draw popup if draw is offered
        if draw_popup:
            pygame.draw.rect(screen, (50, 50, 50), (200, 300, 400, 200))  # Popup background
            pygame.draw.rect(screen, (255, 255, 255), (200, 300, 400, 200), 2)  # Popup border

            popup_text = font.render("Opponent has offered a draw", True, (255, 255, 255))
            screen.blit(popup_text, (230, 330))

            # Draw "Accept" button
            pygame.draw.rect(screen, (0, 200, 0), (290, 400, 100, 40))
            accept_text = button_font.render("Accept", True, (255, 255, 255))
            screen.blit(accept_text, (305, 410))

            # Draw "Reject" button
            pygame.draw.rect(screen, (200, 0, 0), (410, 400, 100, 40))
            reject_text = button_font.render("Reject", True, (255, 255, 255))
            screen.blit(reject_text, (425, 410))

        # Update the game
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

