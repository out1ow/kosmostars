import field
from key_points import *
from ui import *
from units import *
from variable import *


class MainMenuScene:
    def __init__(self):
        self.background = pygame.image.load('sources/background/menu.png')
        self.title = font.render('KOSMOSTARS', True, (128, 128, 128))
        self.ui = pygame.sprite.Group(NewGame(), Continue(), Exit())

    def render(self):
        screen.blit(self.background, (0, 0))
        pygame.draw.rect(screen, BLACK, (420, 170, 242, 80))
        place = self.title.get_rect(center=(544, 200))
        screen.blit(self.title, place)
        self.ui.draw(screen)

    def get_click(self, mouse_pos, board):
        x, y = mouse_pos
        if 471 <= x <= 618 and 279 <= y <= 321:
            variable.game_state = 1
        elif 471 <= x <= 618 and 331 <= y <= 373:
            try:
                board.field.clear()
                board.game_scene.units.empty()
                for _ in range(10):
                    board.field.append([None] * 10)
                board.save.load(board)
            except Exception:
                return
            variable.game_state = 2

            for y in range(1, 11):
                for x in range(1, 11):
                    if board.field[y - 1][x - 1] is not None:
                        unit = board.field[y - 1][x - 1]
                        board.game_scene.units.add(unit)
                        unit.rect.x = x * 64 - 32
                        unit.rect.y = y * 64 - 32
        elif 471 <= x <= 618 and 381 <= y <= 423:
            variable.running = False


class LevelMenuScene:
    def __init__(self):
        self.ui = pygame.sprite.Group(Back(), ChooseLevel(), Level1(), Level2(), Animation())

    def render(self):
        screen.fill(BLACK)
        self.ui.update()
        self.ui.draw(screen)

    def get_click(self, mouse_pos, board):
        x, y = mouse_pos
        if 20 <= x <= 167 and 650 <= y <= 692:
            variable.game_state = 0
        if 174 <= x <= 542 and 100 <= y <= 500:
            variable.game_state = 2

            variable.side = RES
            variable.res_score = 0
            variable.sep_score = 0
            variable.res_count = 0
            variable.sep_count = 0
            board.game_scene.key_point.sprites()[0].change_side()

            board.field.clear()
            board.game_scene.units.empty()
            for _ in range(10):
                board.field.append([None] * 10)
            board.field[0][1] = Trooper(RES)
            board.field[1][0] = Trooper(RES)
            board.field[0][0] = Trooper(RES)

            board.field[9][8] = Trooper(SEP)
            board.field[8][9] = Trooper(SEP)
            board.field[9][9] = Trooper(SEP)

            board.field[7][1] = Box()
            board.field[7][2] = Box()
            board.field[8][2] = Box()
            board.field[1][7] = Box()
            board.field[2][7] = Box()
            board.field[2][8] = Box()

            for y in range(1, 11):
                for x in range(1, 11):
                    if board.field[y - 1][x - 1] is not None:
                        unit = board.field[y - 1][x - 1]
                        board.game_scene.units.add(unit)
                        unit.rect.x = x * 64 - 32
                        unit.rect.y = y * 64 - 32
        if 544 <= x <= 912 and 100 <= y <= 500:
            variable.game_state = 2

            variable.res_score = 0
            variable.sep_score = 0
            variable.res_count = 0
            variable.sep_count = 0
            board.game_scene.key_point.sprites()[0].change_side()

            board.field.clear()
            board.game_scene.units.empty()
            for _ in range(10):
                board.field.append([None] * 10)
            board.field[0][1] = Trooper(RES)
            board.field[1][0] = Trooper(RES)
            board.field[0][0] = Trooper(RES)

            board.field[9][8] = Trooper(SEP)
            board.field[8][9] = Trooper(SEP)
            board.field[9][9] = Trooper(SEP)

            board.field[4][2] = Box()
            board.field[5][2] = Box()
            board.field[6][2] = Box()
            board.field[3][7] = Box()
            board.field[4][7] = Box()
            board.field[5][7] = Box()

            for y in range(1, 11):
                for x in range(1, 11):
                    if board.field[y - 1][x - 1] is not None:
                        unit = board.field[y - 1][x - 1]
                        board.game_scene.units.add(unit)
                        unit.rect.x = x * 64 - 32
                        unit.rect.y = y * 64 - 32


class GameScene:
    def __init__(self):
        self.units = pygame.sprite.Group()
        self.key_point = pygame.sprite.Group(KeyPoint())
        self.ui = pygame.sprite.Group(MakeMove(), GiveUp(), CurrentMove(), UnitMenu(), ScoreFrame())
        self.res_units_cards = pygame.sprite.Group(ResTrooperCard(), ResElitTrooperCard(), ResHeroCard())
        self.sep_units_cards = pygame.sprite.Group(SepTrooperCard(), SepElitTrooperCard(), SepHeroCard())
        self.background = pygame.image.load('sources/background/level.png')
        self.units_cards = self.res_units_cards
        self.score = font.render('', True, (128, 128, 128))

    def render(self):
        screen.blit(self.background, (0, 0))
        self.key_point.draw(screen)
        self.ui.draw(screen)
        self.units_cards.draw(screen)

        for y in range(1, 11):
            for x in range(1, 11):
                if x <= 2 and y <= 2:
                    pygame.draw.rect(screen, BLUE, (x * 64 - 32, y * 64 - 32, 64, 64), 2)
                elif x >= 9 and y >= 9:
                    pygame.draw.rect(screen, RED, (x * 64 - 32, y * 64 - 32, 64, 64), 2)
                else:
                    pygame.draw.rect(screen, WHITE, (x * 64 - 32, y * 64 - 32, 64, 64), 2)
        self.units.draw(screen)

        for unit in self.units.sprites():  # Рисуем полоску хп юнитов
            if type(unit) != Box:
                x, y = unit.rect.x, unit.rect.y
                pygame.draw.rect(screen, RED, (x + 7, y + 5, 50 * (unit.hp / 100), 3))

        pygame.draw.rect(screen, (128, 128, 128), (723, 88, 304, 14))
        pygame.draw.rect(screen, (128, 128, 128), (723, 103, 304, 14))

        pygame.draw.rect(screen, BLUE, (725, 90, 300 * (variable.res_count / 10) + 2, 10))
        pygame.draw.rect(screen, RED, (725, 105, 300 * (variable.sep_count / 10) + 2, 10))

        if side == RES:
            self.score = font.render(str(variable.res_score), True, (128, 128, 128))
        else:
            self.score = font.render(str(variable.sep_score), True, (128, 128, 128))
        screen.blit(self.score, (930, 145))

    def get_click(self, mouse_pos, board):
        x, y = mouse_pos
        cell = field.get_cell_cords(mouse_pos)
        if cell is not None:
            board.on_click(cell)
        else:
            if 900 <= x <= 1047 and 550 <= y <= 592:
                board.change_side()
            elif 900 <= x <= 1047 and 600 <= y <= 642:
                if variable.side == SEP:
                    variable.game_state = 4
                    board.win_scene.background = board.win_scene.res_win_background
                    board.win_scene.total_score = font.render(str(variable.res_score), True, (128, 128, 128))
                    board.win_scene.ui.add(ResWin())
                elif variable.side == RES:
                    variable.game_state = 4
                    board.win_scene.background = board.win_scene.sep_win_background
                    board.win_scene.total_score = font.render(str(variable.sep_score), True, (128, 128, 128))
                    board.win_scene.ui.add(SepWin())

            elif 710 <= x <= 857 and 140 <= y <= 200:
                board.spawn(Trooper(variable.side))
            elif 710 <= x <= 857 and 215 <= y <= 275:
                board.spawn(ElitTrooper(variable.side))
            elif 710 <= x <= 857 and 290 <= y <= 350:
                board.spawn(Hero(variable.side))


class PauseScene:
    def __init__(self):
        self.ui = pygame.sprite.Group(Continue(), Exit())
        self.vertical_borders = pygame.sprite.Group()
        self.horizontal_borders = pygame.sprite.Group()
        self.balls = pygame.sprite.Group()
        self.physics = pygame.sprite.Group(Ball(self.balls, self.horizontal_borders, self.vertical_borders),
                                           Ball(self.balls, self.horizontal_borders, self.vertical_borders),
                                           Ball(self.balls, self.horizontal_borders, self.vertical_borders),
                                           Ball(self.balls, self.horizontal_borders, self.vertical_borders),
                                           Ball(self.balls, self.horizontal_borders, self.vertical_borders))
        Border(self.physics, 5, 5, WIDTH - 5, 5, self.horizontal_borders, self.vertical_borders),
        Border(self.physics, 5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5, self.horizontal_borders, self.vertical_borders),
        Border(self.physics, 5, 5, 5, HEIGHT - 5, self.horizontal_borders, self.vertical_borders),
        Border(self.physics, WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5, self.horizontal_borders, self.vertical_borders)

    def render(self):
        if variable.is_konami:
            self.physics.update()
            screen.fill(BLACK)
            self.physics.draw(screen)
            self.ui.draw(screen)
        else:
            screen.fill(BLACK)
            self.ui.draw(screen)

    def get_click(self, mouse_pos, board):
        x, y = mouse_pos
        if 471 <= x <= 618 and 331 <= y <= 373:
            variable.game_state = 2
            variable.is_konami = False
        elif 471 <= x <= 618 and 381 <= y <= 423:
            variable.game_state = 0
            variable.is_konami = False

            board.save.saving(board)


class WinScene:
    def __init__(self):
        self.res_win_background = pygame.image.load('sources/background/res_win.png')
        self.sep_win_background = pygame.image.load('sources/background/sep_win.png')
        self.background = ''
        self.ui = pygame.sprite.Group(Back(), TotalScore())
        self.total_score = ''

    def render(self):
        screen.blit(self.background, (0, 0))
        self.ui.draw(screen)
        screen.blit(self.total_score, (600, 70))

    def get_click(self, mouse_pos, board):
        x, y = mouse_pos
        if 20 <= x <= 167 and 650 <= y <= 692:
            variable.game_state = 0
            self.ui = pygame.sprite.Group(Back(), TotalScore())
