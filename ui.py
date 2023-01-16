import random

import pygame

import board
from variable import RES, side, RED


class CurrentMove(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.res_sprite = pygame.image.load('sources/sprites/ui/current_move/res_move.png')
        self.sep_sprite = pygame.image.load('sources/sprites/ui/current_move/sep_move.png')
        if side == RES:
            self.image = self.res_sprite
        else:
            self.image = self.sep_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 32

    def change_side(self):
        if self.image == self.res_sprite:
            self.image = self.sep_sprite
        else:
            self.image = self.res_sprite


class ChooseLevel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('sources/sprites/ui/choose_level/choose_level.png')
        self.rect = self.image.get_rect(center=(544, 50))


class ResWin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('sources/sprites/ui/win/res_win.png')
        self.rect = self.image.get_rect(center=(544, 50))


class SepWin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('sources/sprites/ui/win/sep_win.png')
        self.rect = self.image.get_rect(center=(544, 50))


class TotalScore(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('sources/sprites/ui/win/total_win.png')
        self.rect = self.image.get_rect(center=(544, 100))


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/unselected_button.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/selected_button.png')
        self.image = self.unselected_sprite

    def select(self):
        self.image = self.selected_sprite

    def unselect(self):
        self.image = self.unselected_sprite


class MakeMove(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/make_move/unselected_make_move.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/make_move/selected_make_move.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 550


class GiveUp(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/give_up/unselected_give_up.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/give_up/selected_give_up.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 600


class NewGame(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/new_game/unselected_new_game.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/new_game/selected_new_game.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect(center=(544, 300))


class Continue(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/continue/unselected_continue.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/continue/selected_continue.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect(center=(544, 352))


class Exit(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/exit/unselected_exit.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/exit/selected_exit.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect(center=(544, 404))


class Back(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/back/unselected_back.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/back/selected_back.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 650


class Level1(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/level1/unselected_level1.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/level1/selected_level1.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 174
        self.rect.y = 100


class Level2(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/buttons/level2/unselected_level2.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/buttons/level2/selected_level2.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 544
        self.rect.y = 100


class UnitMenu(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('sources/sprites/ui/unit_menu/unit_menu_back.png')
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 130


class UnitCard(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.Surface([0, 0])
        self.selected_sprite = pygame.Surface([0, 0])
        self.image = self.unselected_sprite

    def select(self):
        self.image = self.selected_sprite

    def unselect(self):
        self.image = self.unselected_sprite


class ResTrooperCard(UnitCard):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/res_trooper_card.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/res_trooper_card_selected.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 710
        self.rect.y = 140


class ResElitTrooperCard(UnitCard):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/res_elit_trooper_card.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/res_elit_trooper_card_selected.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 710
        self.rect.y = 215


class ResHeroCard(UnitCard):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/res_hero_card.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/res_hero_card_selected.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 710
        self.rect.y = 290


class SepTrooperCard(UnitCard):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/sep_trooper_card.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/sep_trooper_card_selected.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 710
        self.rect.y = 140


class SepElitTrooperCard(UnitCard):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/sep_elit_trooper_card.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/sep_elit_trooper_card_selected.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 710
        self.rect.y = 215


class SepHeroCard(UnitCard):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/sep_hero_card.png')
        self.selected_sprite = pygame.image.load('sources/sprites/ui/unit_menu/sep_hero_card_selected.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 710
        self.rect.y = 290


class ScoreFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sources/sprites/ui/unit_menu/score.png')
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 140


class Animation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [pygame.image.load('sources/sprites/ui/loading/1.png'),
                       pygame.image.load('sources/sprites/ui/loading/2.png'),
                       pygame.image.load('sources/sprites/ui/loading/3.png'),
                       pygame.image.load('sources/sprites/ui/loading/4.png'),
                       pygame.image.load('sources/sprites/ui/loading/5.png'),
                       pygame.image.load('sources/sprites/ui/loading/6.png'),
                       pygame.image.load('sources/sprites/ui/loading/7.png'),
                       pygame.image.load('sources/sprites/ui/loading/8.png'),
                       pygame.image.load('sources/sprites/ui/loading/9.png'),
                       pygame.image.load('sources/sprites/ui/loading/10.png')
                       ]
        self.rect = self.images[0].get_rect()
        self.rect.x = 900
        self.rect.y = 550

        self.index = 0
        self.image = self.images[self.index]

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


class Ball(pygame.sprite.Sprite):
    def __init__(self, horizontal_borders, vertical_borders):
        super().__init__()
        self.image = pygame.Surface((40, 40), 32)
        pygame.draw.rect(self.image, RED, (0, 0, 40, 40), 20)
        self.rect = pygame.Rect(random.randint(100, 900), random.randint(100, 600), 40, 40)
        self.vx = random.randint(-10, 10)
        self.vy = random.randrange(-10, 10)
        self.borders = [horizontal_borders, vertical_borders]

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, self.borders[0]):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, self.borders[1]):
            self.vx = -self.vx


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, group, x1, y1, x2, y2, horizontal_borders, vertical_borders):
        super().__init__(group)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)