import pygame

from variable import RES


class Unit(pygame.sprite.Sprite):
    #  Класс обычного юнита, от которого наследуются остальные юниты
    def __init__(self, side):
        super().__init__()
        self.side = side  # Сторона конфликта, за которую выступает юнит
        self.hp = 100
        self.damage = 10
        self.attack_distance = 3
        self.move_distance = 1  # Дальность передвижения юнита
        self.cost = 100  # Стоимость юнита в боевых очках
        self.is_moved = False
        self.is_attacked = False

    def get_side(self):  # Возвращает сторону конфликта юнита
        return self.side

    def can_move(self, board, cell1, cell2):  # Проверяет может ли юнит походить в выбранную клетку
        x1, y1 = cell1
        x2, y2 = cell2
        if board.field[y2][x2] == board.field[y1][x1]:  # Юнит может остаться на месте
            return True
        if board.field[y2][x2] is not None:  # Если целевая клетка занята
            return False
        if abs(x2 - x1) <= self.move_distance and y2 == y1:  # Если растояние больше чем move_distance
            return True
        elif x1 == x2 and abs(y2 - y1) <= self.move_distance:
            return True
        return False

    def can_attack(self, board, cell1, cell2):  # Проверяет может ли юнит атаковать выбранную клетку
        x1, y1 = cell1
        x2, y2 = cell2
        if board.field[y2][x2] == board.field[y1][x1]:  # Можно ничего не атаковать
            return True
        if board.field[y2][x2] is None:  # Если целевая клетка пуста
            return False
        if board.field[y2][x2].get_side() == self.get_side():  # Если целевая клетк занята вражеским юнитом
            return False
        if abs(x2 - x1) <= self.attack_distance and y2 == y1:  # Если расстояние соответствует attack_distance
            return True
        elif x1 == x2 and abs(y2 - y1) <= self.attack_distance:
            return True
        elif abs(x2 - x1) <= self.attack_distance and abs(y2 - y1) <= self.attack_distance:
            return True
        return False

    def is_dead(self):
        if self.hp <= 0:
            return True
        return False


class Trooper(Unit):  # Класс обычного штурмовика
    def __init__(self, side):
        super().__init__(side)
        self.hp = 100
        self.damage = 20
        self.attack_distance = 3
        self.move_distance = 2
        self.cost = 100

        if self.side == RES:
            self.image = pygame.image.load('C:/Users/polee/PycharmProjects/sw_bf_3/sources'
                                           '/sprites/res_trooper/idle.png')
        else:
            self.image = pygame.image.load('C:/Users/polee/PycharmProjects/sw_bf_3/sources'
                                           '/sprites/sep_trooper/idle.png')
        self.rect = self.image.get_rect()


class ElitTrooper(Unit):  # Класс элитного штурмовика
    def __init__(self, side):
        super().__init__(side)
        self.hp = 100
        self.damage = 30
        self.attack_distance = 3
        self.move_distance = 2
        self.cost = 200

        if self.side == RES:
            self.image = pygame.image.load('C:/Users/polee/PycharmProjects/sw_bf_3/sources'
                                           '/sprites/res_elite_trooper/idle.png')
        else:
            self.image = pygame.image.load('C:/Users/polee/PycharmProjects/sw_bf_3/sources'
                                           '/sprites/sep_elit_trooper/idle.png')
        self.rect = self.image.get_rect()


class Hero(Unit):  # Класс героя
    def __init__(self, side):
        super().__init__(side)
        self.hp = 100
        self.damage = 50
        self.attack_distance = 1
        self.move_distance = 2
        self.cost = 400

        if self.side == RES:
            self.image = pygame.image.load('C:/Users/polee/PycharmProjects/sw_bf_3/sources'
                                           '/sprites/res_hero/idle.png')
        else:
            self.image = pygame.image.load('C:/Users/polee/PycharmProjects/sw_bf_3/sources'
                                           '/sprites/sep_hero/idle.png')
        self.rect = self.image.get_rect()
