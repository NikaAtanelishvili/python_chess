import pygame

from board import Board

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Chess Game')

    board = Board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        board.draw_board(screen)

        # Update the game
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

