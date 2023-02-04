import variable
from save import Saves
from scenes import *


def get_cell_cords(mouse_pos):
    x, y = mouse_pos
    if 672 < x or x < 32 or 672 < y or y < 32:
        return None
    return (x - 32) // 64, (y - 32) // 64


class Board:
    def __init__(self):

        self.field = []

        self.save = Saves()

        self.selected_unit = None
        self.selected_cell = None

        self.main_menu_scene = MainMenuScene()
        self.level_menu_scene = LevelMenuScene()
        self.game_scene = GameScene()
        self.pause_scene = PauseScene()
        self.win_scene = WinScene()

    def render(self):
        if variable.game_state == 0:
            self.main_menu_scene.render()

        elif variable.game_state == 1:
            self.level_menu_scene.render()

        elif variable.game_state == 2:
            self.game_scene.render()

            if self.selected_unit is not None:
                self.on_click(self.selected_unit)

        elif variable.game_state == 3:
            self.pause_scene.render()

        elif variable.game_state == 4:
            self.win_scene.render()

    def change_side(self):
        variable.side = 1 - variable.side

        self.game_scene.ui.sprites()[2].change_side()

        for i in self.game_scene.units.sprites():
            i.is_moved = False
            i.is_attacked = False

        flag = set()
        for i in [(4, 4), (4, 5), (5, 5), (5, 4)]:
            x, y = i
            if self.field[y][x] is not None:
                flag.add(self.field[y][x].get_side())

        if len(flag) > 1:  # Если в пределах контрольной точки находятся юниты разных сторон
            self.game_scene.key_point.sprites()[0].change_side()
        elif self.field[4][4] is not None:
            self.game_scene.key_point.sprites()[0].change_side(self.field[4][4].get_side())
        elif self.field[4][5] is not None:
            self.game_scene.key_point.sprites()[0].change_side(self.field[4][5].get_side())
        elif self.field[5][4] is not None:
            self.game_scene.key_point.sprites()[0].change_side(self.field[5][4].get_side())
        elif self.field[5][5] is not None:
            self.game_scene.key_point.sprites()[0].change_side(self.field[5][5].get_side())
        else:
            self.game_scene.key_point.sprites()[0].change_side()

        if variable.side == RES:
            self.game_scene.units_cards = self.game_scene.res_units_cards
            variable.res_score += 10
        else:
            self.game_scene.units_cards = self.game_scene.sep_units_cards
            variable.sep_score += 10
            variable.total_score += 10

        if variable.res_count == 10:
            variable.game_state = 4
            self.win_scene.background = self.win_scene.res_win_background
            self.win_scene.ui.add(ResWin())
        elif variable.sep_count == 10:
            variable.game_state = 4
            self.win_scene.background = self.win_scene.sep_win_background
            self.win_scene.ui.add(SepWin())

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
                    self.game_scene.units.add(unit)
                    unit.rect.x = 1 * 64 - 32
                    unit.rect.y = 1 * 64 - 32
                elif self.field[1][0] is None:
                    self.field[1][0] = unit
                    variable.res_score -= unit.cost
                    self.game_scene.units.add(unit)
                    unit.rect.x = 1 * 64 - 32
                    unit.rect.y = 2 * 64 - 32
                elif self.field[0][1] is None:
                    self.field[0][1] = unit
                    variable.res_score -= unit.cost
                    self.game_scene.units.add(unit)
                    unit.rect.x = 2 * 64 - 32
                    unit.rect.y = 1 * 64 - 32
                elif self.field[1][1] is None:
                    self.field[1][1] = unit
                    variable.res_score -= unit.cost
                    self.game_scene.units.add(unit)
                    unit.rect.x = 2 * 64 - 32
                    unit.rect.y = 2 * 64 - 32
        else:
            if variable.sep_score >= unit.cost:
                if self.field[8][8] is None:
                    self.field[8][8] = unit
                    variable.sep_score -= unit.cost
                    self.game_scene.units.add(unit)
                    unit.rect.x = 9 * 64 - 32
                    unit.rect.y = 9 * 64 - 32
                elif self.field[9][8] is None:
                    self.field[9][8] = unit
                    variable.sep_score -= unit.cost
                    self.game_scene.units.add(unit)
                    unit.rect.x = 9 * 64 - 32
                    unit.rect.y = 10 * 64 - 32
                elif self.field[8][9] is None:
                    self.field[8][9] = unit
                    variable.sep_score -= unit.cost
                    self.game_scene.units.add(unit)
                    unit.rect.x = 10 * 64 - 32
                    unit.rect.y = 9 * 64 - 32
                elif self.field[9][9] is None:
                    self.field[9][9] = unit
                    variable.sep_score -= unit.cost
                    self.game_scene.units.add(unit)
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
            variable.res_score += 20
            variable.total_score += 20
        else:
            variable.sep_score += 20

        if self.field[y2][x2].is_dead():
            self.kill_unit(target_cell)

    def kill_unit(self, cell):
        x, y = cell
        self.field[y][x].kill()
        self.field[y][x] = None

        if side == RES:
            variable.res_score += 50
            variable.total_score += 50
        else:
            variable.sep_score += 50

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
        if variable.game_state == 0:
            self.main_menu_scene.get_click(mouse_pos, self)

        elif variable.game_state == 1:
            self.level_menu_scene.get_click(mouse_pos, self)

        elif variable.game_state == 2:
            self.game_scene.get_click(mouse_pos, self)

        elif variable.game_state == 3:
            self.pause_scene.get_click(mouse_pos, self)

        elif variable.game_state == 4:
            self.win_scene.get_click(mouse_pos, self)
