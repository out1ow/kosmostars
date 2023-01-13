import pygame

from variable import RES, side


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
