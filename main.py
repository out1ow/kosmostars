import pygame

from board import Board
from variable import screen, FPS


def main():
    game_state = 1

    if game_state == 1:
        board = Board()
        clock = pygame.time.Clock()
        running = True
        board.render()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 900 <= x <= 1047 and 550 <= y <= 592:
                        board.all_ui.sprites()[0].select()
                    else:
                        board.all_ui.sprites()[0].unselect()

                    if 900 <= x <= 1047 and 600 <= y <= 642:
                        board.all_ui.sprites()[1].select()
                    else:
                        board.all_ui.sprites()[1].unselect()
                    board.all_ui.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()


if __name__ == '__main__':
    main()
