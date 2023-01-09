import pygame

import variable
from key_point import KeyPoint
from ui import CurrentMove, MakeMove, GiveUp
from units import Trooper, ElitTrooper, Hero
from variable import RES, SEP, BLACK, screen, WHITE, GREEN, RED


class Board:  # Класс игрового поля
    def __init__(self):
        self.field = []
        for _ in range(10):
            self.field.append([None] * 10)  # Список содержащий все клетки поля
        self.field[0][0] = Trooper(RES)
        self.field[1][0] = ElitTrooper(RES)
        self.field[2][0] = Hero(RES)

        self.field[0][3] = ElitTrooper(SEP)
        self.field[1][3] = Trooper(SEP)
        self.field[2][3] = Hero(SEP)

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
        self.all_ui = pygame.sprite.Group(MakeMove(), GiveUp(), CurrentMove())

    def render(self):
        screen.fill(BLACK)
        self.all_key_points.draw(screen)
        self.all_ui.draw(screen)
        for y in range(1, 11):
            for x in range(1, 11):
                pygame.draw.rect(screen, WHITE, (x * 64 - 32, y * 64 - 32, 64, 64), 1)
        self.all_units.draw(screen)

    def change_side(self):
        variable.side = 1 - variable.side

        self.all_ui.sprites()[2].change_side()

        for i in self.all_units.sprites():
            i.is_moved = False
            i.is_attacked = False

    def spawn(self, cell, side, unit_class):  # Спавнит нового юнита в конкретной точке
        pass

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
