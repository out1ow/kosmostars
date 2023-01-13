import pygame

import variable
from key_point import KeyPoint
from ui import *
from units import Trooper, ElitTrooper, Hero
from variable import RES, SEP, BLACK, screen, WHITE, GREEN, RED, BLUE, font


class Board:  # Класс игрового поля
    def __init__(self):
        self.field = []
        for _ in range(10):
            self.field.append([None] * 10)  # Список содержащий все клетки поля
        self.field[0][1] = Trooper(RES)
        self.field[1][0] = ElitTrooper(RES)
        self.field[0][0] = Hero(RES)

        self.field[9][8] = ElitTrooper(SEP)
        self.field[8][9] = Trooper(SEP)
        self.field[9][9] = Hero(SEP)

        self.selected_unit = None
        self.selected_cell = None

        self.all_units = pygame.sprite.Group()
        for y in range(1, 11):
            for x in range(1, 11):
                if self.field[y - 1][x - 1] is not None:
                    unit = self.field[y - 1][x - 1]
                    self.all_units.add(unit)
                    unit.rect.x = x * 64 - 32
                    unit.rect.y = y * 64 - 32

        self.all_key_points = pygame.sprite.Group(KeyPoint())
        self.all_ui = pygame.sprite.Group(MakeMove(), GiveUp(), CurrentMove(), UnitMenu(), ScoreFrame())

        self.res_units_cards = pygame.sprite.Group(ResTrooperCard(), ResElitTrooperCard(), ResHeroCard())
        self.sep_units_cards = pygame.sprite.Group(SepTrooperCard(), SepElitTrooperCard(), SepHeroCard())
        self.units_cards = self.res_units_cards

        self.background = pygame.image.load('sources/background/2.png')

        self.text = font.render('0', True, (128, 128, 128))

    def render(self):
        screen.blit(self.background, (0, 0))
        self.all_key_points.draw(screen)
        self.all_ui.draw(screen)
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
            x, y = unit.rect.x, unit.rect.y
            pygame.draw.rect(screen, RED, (x + 7, y + 5, 50 * (unit.hp / 100), 3))

        pygame.draw.rect(screen, (128, 128, 128), (723, 88, 304, 14))
        pygame.draw.rect(screen, (128, 128, 128), (723, 103, 304, 14))

        pygame.draw.rect(screen, BLUE, (725, 90, 300 * (variable.res_count / 10) + 2, 10))
        pygame.draw.rect(screen, RED, (725, 105, 300 * (variable.sep_count / 10) + 2, 10))

        if variable.side == RES:
            self.text = font.render(str(variable.res_score), True, (128, 128, 128))
        else:
            self.text = font.render(str(variable.sep_score), True, (128, 128, 128))
        screen.blit(self.text, (930, 143))

    def change_side(self):
        variable.side = 1 - variable.side

        self.all_ui.sprites()[2].change_side()
        variable.move_count += 1

        for i in self.all_units.sprites():
            i.is_moved = False
            i.is_attacked = False

        flag = set()
        for i in [(4, 4), (4, 5), (5, 5), (5, 4)]:
            x, y = i
            if self.field[y][x] is not None:
                flag.add(self.field[y][x].get_side())

        if len(flag) > 1:  # Если в пределах контрольной точки находятся юниты разных сторон
            self.all_key_points.sprites()[0].change_side()
        elif self.field[4][4] is not None:
            self.all_key_points.sprites()[0].change_side(self.field[4][4].get_side())
        elif self.field[4][5] is not None:
            self.all_key_points.sprites()[0].change_side(self.field[4][5].get_side())
        elif self.field[5][4] is not None:
            self.all_key_points.sprites()[0].change_side(self.field[5][4].get_side())
        elif self.field[5][5] is not None:
            self.all_key_points.sprites()[0].change_side(self.field[5][5].get_side())
        else:
            self.all_key_points.sprites()[0].change_side()

        if variable.side == RES:
            self.units_cards = self.res_units_cards
            variable.sep_score += 50
        else:
            self.units_cards = self.sep_units_cards
            variable.res_score += 50

        self.render()

    def spawn(self, unit):  # Спавнит нового юнита в конкретной точке
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

        self.render()

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

        if self.field[y2][x2].is_dead():
            self.kill_unit(target_cell)

    def kill_unit(self, cell):
        x, y = cell
        self.field[y][x].kill()
        self.field[y][x] = None

    def get_cell_cords(self, mouse_pos):
        x, y = mouse_pos
        if 672 < x or x < 32 or 672 < y or y < 32:
            return None
        return (x - 32) // 64, (y - 32) // 64

    def on_click(self, cell):
        if self.selected_unit is None and self.selected_cell is None:
            x1, y1 = cell
            if self.field[y1][x1] is not None:
                if self.field[y1][x1].get_side() == variable.side:
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
        elif self.selected_unit is not None and self.selected_cell is None:
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
            self.render()

    def get_click(self, mouse_pos):
        self.render()
        cell = self.get_cell_cords(mouse_pos)
        if cell is not None:
            self.on_click(cell)
        else:
            x, y = mouse_pos
            if 900 <= x <= 1047 and 550 <= y <= 592:
                self.change_side()
            elif 900 <= x <= 1047 and 600 <= y <= 642:
                pass

            elif 710 <= x <= 857 and 140 <= y <= 200:
                self.spawn(Trooper(variable.side))
            elif 710 <= x <= 857 and 215 <= y <= 275:
                self.spawn(ElitTrooper(variable.side))
            elif 710 <= x <= 857 and 290 <= y <= 350:
                self.spawn(Hero(variable.side))
