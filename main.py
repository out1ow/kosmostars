import variable
from field import Board
from variable import FPS, KONAMI, pygame


def main():
    board = Board()
    clock = pygame.time.Clock()
    code = []
    index = 0
    while variable.running:
        if variable.game_state == 0:  # Стартовое меню
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    variable.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 471 <= x <= 618 and 279 <= y <= 321:
                        board.all_menu_ui.sprites()[0].select()
                    else:
                        board.all_menu_ui.sprites()[0].unselect()
                    if 471 <= x <= 618 and 331 <= y <= 373:
                        board.all_menu_ui.sprites()[1].select()
                    else:
                        board.all_menu_ui.sprites()[1].unselect()
                    if 471 <= x <= 618 and 381 <= y <= 423:
                        board.all_menu_ui.sprites()[2].select()
                    else:
                        board.all_menu_ui.sprites()[2].unselect()

        elif variable.game_state == 1:  # Экран выбора уровня
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    variable.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 20 <= x <= 167 and 650 <= y <= 692:
                        board.all_level_menu_ui.sprites()[0].select()
                    else:
                        board.all_level_menu_ui.sprites()[0].unselect()
                    if 174 <= x <= 542 and 100 <= y <= 500:
                        board.all_level_menu_ui.sprites()[2].select()
                    else:
                        board.all_level_menu_ui.sprites()[2].unselect()
                    if 544 <= x <= 912 and 100 <= y <= 500:
                        board.all_level_menu_ui.sprites()[3].select()
                    else:
                        board.all_level_menu_ui.sprites()[3].unselect()

        elif variable.game_state == 2:  # Основной игровой процес
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    variable.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        variable.game_state = 3
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 900 <= x <= 1047 and 550 <= y <= 592:
                        board.all_level_ui.sprites()[0].select()
                    else:
                        board.all_level_ui.sprites()[0].unselect()
                    if 900 <= x <= 1047 and 600 <= y <= 642:
                        board.all_level_ui.sprites()[1].select()
                    else:
                        board.all_level_ui.sprites()[1].unselect()

                    if 710 <= x <= 857 and 140 <= y <= 200:
                        board.units_cards.sprites()[0].select()
                    else:
                        board.units_cards.sprites()[0].unselect()
                    if 710 <= x <= 857 and 215 <= y <= 275:
                        board.units_cards.sprites()[1].select()
                    else:
                        board.units_cards.sprites()[1].unselect()
                    if 710 <= x <= 857 and 290 <= y <= 350:
                        board.units_cards.sprites()[2].select()
                    else:
                        board.units_cards.sprites()[2].unselect()

        elif variable.game_state == 3:  # Экран паузы
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    variable.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 471 <= x <= 618 and 331 <= y <= 373:
                        board.all_pause_ui.sprites()[0].select()
                    else:
                        board.all_pause_ui.sprites()[0].unselect()
                    if 471 <= x <= 618 and 381 <= y <= 423:
                        board.all_pause_ui.sprites()[1].select()
                    else:
                        board.all_pause_ui.sprites()[1].unselect()
                elif event.type == pygame.KEYDOWN:
                    if event.key == KONAMI[index]:
                        code.append(event.key)
                        index += 1
                        if code == KONAMI:
                            index = 0
                            variable.is_konami = True
                    else:
                        code = []
                        index = 0

        elif variable.game_state == 4:  # Экран победы
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    variable.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    board.get_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 20 <= x <= 167 and 650 <= y <= 692:
                        board.all_win_ui.sprites()[0].select()
                    else:
                        board.all_win_ui.sprites()[0].unselect()

        board.render()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
