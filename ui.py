import pygame

from variable import RES, side


class CurrentMove(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.res_sprite = pygame.image.load('sources/sprites/current_move/res_move.png')
        self.sep_sprite = pygame.image.load('sources/sprites/current_move/sep_move.png')
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


class Button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/buttons/unselected_button.png')
        self.selected_sprite = pygame.image.load('sources/sprites/buttons/selected_button.png')
        self.image = self.unselected_sprite

    def select(self):
        self.image = self.selected_sprite

    def unselect(self):
        self.image = self.unselected_sprite


class MakeMove(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/buttons/make_move/unselected_make_move.png')
        self.selected_sprite = pygame.image.load('sources/sprites/buttons/make_move/selected_make_move.png')
        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 550


class GiveUp(Button):
    def __init__(self):
        super().__init__()

        self.unselected_sprite = pygame.image.load('sources/sprites/buttons/give_up/unselected_give_up.png')
        self.selected_sprite = pygame.image.load('sources/sprites/buttons/give_up/selected_give_up.png')

        self.image = self.unselected_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 900
        self.rect.y = 600
