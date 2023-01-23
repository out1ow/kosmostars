import pygame

import variable
from save import Saves
from variable import *
from key_points import *
from ui import *
from units import *


class Board:  # Класс игрового поля
    def __init__(self):

        self.field = []

        self.save = Saves()

        self.selected_unit = None
        self.selected_cell = None

        self.all_units = pygame.sprite.Group()

        self.key_point = pygame.sprite.Group(KeyPoint())
        self.all_level_ui = pygame.sprite.Group(MakeMove(), GiveUp(), CurrentMove(), UnitMenu(), ScoreFrame())
        self.res_units_cards = pygame.sprite.Group(ResTrooperCard(), ResElitTrooperCard(), ResHeroCard())
        self.sep_units_cards = pygame.sprite.Group(SepTrooperCard(), SepElitTrooperCard(), SepHeroCard())
        self.background = pygame.image.load('sources/background/level.png')
        self.units_cards = self.res_units_cards
        self.score = font.render('', True, (128, 128, 128))

        self.background_menu = pygame.image.load('sources/background/menu.png')
        self.title = font.render('KOSMOSTARS', True, (128, 128, 128))
        self.all_menu_ui = pygame.sprite.Group(NewGame(), Continue(), Exit())

        self.all_level_menu_ui = pygame.sprite.Group(Back(), ChooseLevel(), Level1(), Level2(), Animation())

        self.res_win_background = pygame.image.load('sources/background/res_win.png')
        self.sep_win_background = pygame.image.load('sources/background/sep_win.png')
        self.background_win = ''
        self.all_win_ui = pygame.sprite.Group(Back(), TotalScore())
        self.total_score = ''

        self.all_pause_ui = pygame.sprite.Group(Continue(), Exit())
        self.vertical_borders = pygame.sprite.Group()
        self.horizontal_borders = pygame.sprite.Group()
        self.physics = pygame.sprite.Group(Ball(self.horizontal_borders, self.vertical_borders),
                                           Ball(self.horizontal_borders, self.vertical_borders),
                                           Ball(self.horizontal_borders, self.vertical_borders),
                                           Ball(self.horizontal_borders, self.vertical_borders),
                                           Ball(self.horizontal_borders, self.vertical_borders),
                                           Ball(self.horizontal_borders, self.vertical_borders),
                                           Ball(self.horizontal_borders, self.vertical_borders),
                                           Ball(self.horizontal_borders, self.vertical_borders),
                                           Ball(self.horizontal_borders, self.vertical_borders))
        Border(self.physics, 5, 5, WIDTH - 5, 5, self.horizontal_borders, self.vertical_borders),
        Border(self.physics, 5, HEIGHT - 5, WIDTH - 5, HEIGHT - 5, self.horizontal_borders, self.vertical_borders),
        Border(self.physics, 5, 5, 5, HEIGHT - 5, self.horizontal_borders, self.vertical_borders),
        Border(self.physics, WIDTH - 5, 5, WIDTH - 5, HEIGHT - 5, self.horizontal_borders, self.vertical_borders)

    def render(self):
        if variable.game_state == 0:
            screen.blit(self.background_menu, (0, 0))
            pygame.draw.rect(screen, BLACK, (420, 170, 242, 80))
            place = self.title.get_rect(center=(544, 200))
            screen.blit(self.title, place)
            self.all_menu_ui.draw(screen)

        elif variable.game_state == 1:
            screen.fill(BLACK)
            self.all_level_menu_ui.update()
            self.all_level_menu_ui.draw(screen)

        elif variable.game_state == 2:
            screen.blit(self.background, (0, 0))
            self.key_point.draw(screen)
            self.all_level_ui.draw(screen)
            self.units_cards.draw(screen)

            for y in range(1, 11):
                for x in range(1, 11):
                    if x <= 2 and y <= 2:
                        pygame.draw.rect(screen, BLUE, (x * 64 - 32, y * 64 - 32, 64, 64), 2)
                    elif x >= 9 and y >= 9:
                        pygame.draw.rect(screen, RED, (x * 64 - 32, y * 64 - 32, 64, 64), 2)
                    else:
                        pygame.draw.rect(screen, WHITE, (x * 64 - 32, y * 64 - 32, 64, 64), 2)
            self.all_units.draw(screen)

            for unit in self.all_units.sprites():  # Рисуем полоску хп юнитов
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

            if self.selected_unit is not None:
                self.on_click(self.selected_unit)

        elif variable.game_state == 3:
            if variable.is_konami:
                self.physics.update()
                screen.fill(BLACK)
                self.physics.draw(screen)
                self.all_pause_ui.draw(screen)
            else:
                screen.fill(BLACK)
                self.all_pause_ui.draw(screen)

        elif variable.game_state == 4:
            screen.blit(self.background_win, (0, 0))
            self.all_win_ui.draw(screen)
            self.total_score = font.render(str(variable.total_score), True, (128, 128, 128))
            screen.blit(self.total_score, (600, 70))

    def change_side(self):
        variable.side = 1 - variable.side

        self.all_level_ui.sprites()[2].change_side()

        for i in self.all_units.sprites():
            i.is_moved = False
            i.is_attacked = False

        flag = set()
        for i in [(4, 4), (4, 5), (5, 5), (5, 4)]:
            x, y = i
            if self.field[y][x] is not None:
                flag.add(self.field[y][x].get_side())

        if len(flag) > 1:  # Если в пределах контрольной точки находятся юниты разных сторон
            self.key_point.sprites()[0].change_side()
        elif self.field[4][4] is not None:
            self.key_point.sprites()[0].change_side(self.field[4][4].get_side())
        elif self.field[4][5] is not None:
            self.key_point.sprites()[0].change_side(self.field[4][5].get_side())
        elif self.field[5][4] is not None:
            self.key_point.sprites()[0].change_side(self.field[5][4].get_side())
        elif self.field[5][5] is not None:
            self.key_point.sprites()[0].change_side(self.field[5][5].get_side())
        else:
            self.key_point.sprites()[0].change_side()

        if variable.side == RES:
            self.units_cards = self.res_units_cards
            variable.res_score += 50
        else:
            self.units_cards = self.sep_units_cards
            variable.sep_score += 50
            variable.total_score += 50

        if variable.res_count == 10:
            variable.game_state = 4
            self.background_win = self.res_win_background
            self.all_win_ui.add(ResWin())
        elif variable.sep_count == 10:
            variable.game_state = 4
            self.background_win = self.sep_win_background
            self.all_win_ui.add(SepWin())

    def spawn(self, unit):  # Спавнит нового юнита в конкретной точке
        if type(unit) == Hero:
            for i in self.field:
                for j in i:
                    if type(j) == Hero and j.get_side() == variable.side:
                        return
        if variable.side == RES:
            if variable.res_score >= unit.cost:
                if self.field[0][0] is None:
                    self.field[0][0] = unit
                    variable.res_score -= unit.cost
                    self.all_units.add(unit)
                    unit.rect.x = 1 * 64 - 32
                    unit.rect.y = 1 * 64 - 32
                elif self.field[1][0] is None:
                    self.field[1][0] = unit
                    variable.res_score -= unit.cost
                    self.all_units.add(unit)
                    unit.rect.x = 1 * 64 - 32
                    unit.rect.y = 2 * 64 - 32
                elif self.field[0][1] is None:
                    self.field[0][1] = unit
                    variable.res_score -= unit.cost
                    self.all_units.add(unit)
                    unit.rect.x = 2 * 64 - 32
                    unit.rect.y = 1 * 64 - 32
                elif self.field[1][1] is None:
                    self.field[1][1] = unit
                    variable.res_score -= unit.cost
                    self.all_units.add(unit)
                    unit.rect.x = 2 * 64 - 32
                    unit.rect.y = 2 * 64 - 32
        else:
            if variable.sep_score >= unit.cost:
                if self.field[8][8] is None:
                    self.field[8][8] = unit
                    variable.sep_score -= unit.cost
                    self.all_units.add(unit)
                    unit.rect.x = 9 * 64 - 32
                    unit.rect.y = 9 * 64 - 32
                elif self.field[9][8] is None:
                    self.field[9][8] = unit
                    variable.sep_score -= unit.cost
                    self.all_units.add(unit)
                    unit.rect.x = 9 * 64 - 32
                    unit.rect.y = 10 * 64 - 32
                elif self.field[8][9] is None:
                    self.field[8][9] = unit
                    variable.sep_score -= unit.cost
                    self.all_units.add(unit)
                    unit.rect.x = 10 * 64 - 32
                    unit.rect.y = 9 * 64 - 32
                elif self.field[9][9] is None:
                    self.field[9][9] = unit
                    variable.sep_score -= unit.cost
                    self.all_units.add(unit)
                    unit.rect.x = 10 * 64 - 32
                    unit.rect.y = 10 * 64 - 32

    def move_unit(self, cell1, cell2):
        x1, y1 = cell1
        x2, y2 = cell2
        unit = self.field[y1][x1]
        unit.is_moved = True
        unit.rect.x = x2 * 64 + 32
        unit.rect.y = y2 * 64 + 32
        self.field[y1][x1] = None
        self.field[y2][x2] = unit

    def attack_unit(self, attacking_cell, target_cell):
        x1, y1 = attacking_cell
        x2, y2 = target_cell
        self.field[y1][x1].is_attacked = True
        self.field[y2][x2].hp -= self.field[y1][x1].damage

        if side == RES:
            variable.res_score += 10
            variable.total_score += 10
        else:
            variable.sep_score += 10

        if self.field[y2][x2].is_dead():
            self.kill_unit(target_cell)

    def kill_unit(self, cell):
        x, y = cell
        self.field[y][x].kill()
        self.field[y][x] = None

        if side == RES:
            variable.res_score += 20
            variable.total_score += 20
        else:
            variable.sep_score += 20

    def get_cell_cords(self, mouse_pos):
        x, y = mouse_pos
        if 672 < x or x < 32 or 672 < y or y < 32:
            return None
        return (x - 32) // 64, (y - 32) // 64

    def on_click(self, cell):
        x1, y1 = cell
        if self.field[y1][x1] is not None and self.field[y1][x1].get_side() == variable.side:
            self.selected_unit = cell
            unit = self.field[y1][x1]
            for x2 in range(10):
                for y2 in range(10):
                    if not unit.is_moved:  # двигаем
                        if unit.can_move(self, cell, (x2, y2)):
                            pygame.draw.circle(screen, GREEN, ((x2 + 1) * 64, (y2 + 1) * 64), 32, 3)
                    elif unit.is_moved and not unit.is_attacked:  # Атакуем
                        if unit.can_attack(self, cell, (x2, y2)):
                            pygame.draw.circle(screen, RED, ((x2 + 1) * 64, (y2 + 1) * 64), 32, 3)
        elif self.selected_unit is not None:
            self.selected_cell = cell
            x, y = self.selected_unit
            unit = self.field[y][x]
            if not unit.is_moved:
                if unit.can_move(self, self.selected_unit, self.selected_cell):
                    self.move_unit(self.selected_unit, self.selected_cell)
            elif unit.is_moved and not unit.is_attacked:
                if unit.can_attack(self, self.selected_unit, self.selected_cell):
                    self.attack_unit(self.selected_unit, self.selected_cell)
            self.selected_cell = None
            self.selected_unit = None

    def get_click(self, mouse_pos):
        x, y = mouse_pos
        if variable.game_state == 0:
            if 471 <= x <= 618 and 279 <= y <= 321:
                variable.game_state = 1
            elif 471 <= x <= 618 and 331 <= y <= 373:
                variable.game_state = 2

                self.field.clear()
                self.all_units.empty()
                for _ in range(10):
                    self.field.append([None] * 10)

                self.save.load(self)

                for y in range(1, 11):
                    for x in range(1, 11):
                        if self.field[y - 1][x - 1] is not None:
                            unit = self.field[y - 1][x - 1]
                            self.all_units.add(unit)
                            unit.rect.x = x * 64 - 32
                            unit.rect.y = y * 64 - 32
            elif 471 <= x <= 618 and 381 <= y <= 423:
                variable.running = False

        elif variable.game_state == 1:
            if 20 <= x <= 167 and 650 <= y <= 692:
                variable.game_state = 0
            if 174 <= x <= 542 and 100 <= y <= 500:
                variable.game_state = 2

                variable.res_score = 0
                variable.sep_score = 0
                variable.res_count = 0
                variable.sep_count = 0
                variable.total_score = 0

                self.field.clear()
                self.all_units.empty()
                for _ in range(10):
                    self.field.append([None] * 10)
                self.field[0][1] = Trooper(RES)
                self.field[1][0] = Trooper(RES)
                self.field[0][0] = Trooper(RES)

                self.field[9][8] = Trooper(SEP)
                self.field[8][9] = Trooper(SEP)
                self.field[9][9] = Trooper(SEP)

                self.field[7][1] = Box()
                self.field[7][2] = Box()
                self.field[8][2] = Box()
                self.field[1][7] = Box()
                self.field[2][7] = Box()
                self.field[2][8] = Box()

                for y in range(1, 11):
                    for x in range(1, 11):
                        if self.field[y - 1][x - 1] is not None:
                            unit = self.field[y - 1][x - 1]
                            self.all_units.add(unit)
                            unit.rect.x = x * 64 - 32
                            unit.rect.y = y * 64 - 32
            if 544 <= x <= 912 and 100 <= y <= 500:
                variable.game_state = 2

                variable.res_score = 0
                variable.sep_score = 0
                variable.res_count = 0
                variable.sep_count = 0
                variable.total_score = 0

                self.field.clear()
                self.all_units.empty()
                for _ in range(10):
                    self.field.append([None] * 10)
                self.field[0][1] = Trooper(RES)
                self.field[1][0] = Trooper(RES)
                self.field[0][0] = Trooper(RES)

                self.field[9][8] = Trooper(SEP)
                self.field[8][9] = Trooper(SEP)
                self.field[9][9] = Trooper(SEP)

                self.field[4][2] = Box()
                self.field[5][2] = Box()
                self.field[6][2] = Box()
                self.field[3][7] = Box()
                self.field[4][7] = Box()
                self.field[5][7] = Box()

                for y in range(1, 11):
                    for x in range(1, 11):
                        if self.field[y - 1][x - 1] is not None:
                            unit = self.field[y - 1][x - 1]
                            self.all_units.add(unit)
                            unit.rect.x = x * 64 - 32
                            unit.rect.y = y * 64 - 32

        elif variable.game_state == 2:
            cell = self.get_cell_cords(mouse_pos)
            if cell is not None:
                self.on_click(cell)
            else:
                if 900 <= x <= 1047 and 550 <= y <= 592:
                    self.change_side()
                elif 900 <= x <= 1047 and 600 <= y <= 642:
                    variable.game_state = 4
                    self.background_win = self.sep_win_background
                    self.all_win_ui.add(SepWin())

                elif 710 <= x <= 857 and 140 <= y <= 200:
                    self.spawn(Trooper(variable.side))
                elif 710 <= x <= 857 and 215 <= y <= 275:
                    self.spawn(ElitTrooper(variable.side))
                elif 710 <= x <= 857 and 290 <= y <= 350:
                    self.spawn(Hero(variable.side))

        elif variable.game_state == 3:
            if 471 <= x <= 618 and 331 <= y <= 373:
                variable.game_state = 2
                variable.is_konami = False
            elif 471 <= x <= 618 and 381 <= y <= 423:
                variable.game_state = 0
                variable.is_konami = False

                self.save.saving(self)
        elif variable.game_state == 4:
            if 20 <= x <= 167 and 650 <= y <= 692:
                variable.game_state = 0
                self.all_win_ui = pygame.sprite.Group(Back(), TotalScore())
