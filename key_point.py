import pygame

from variable import RES, SEP


class KeyPoint(pygame.sprite.Sprite):
    # Класс контрольной точки
    def __init__(self):
        super().__init__()

        self.res_sprite = pygame.image.load('sources/sprites/key_points/res_point.png')
        self.sep_sprite = pygame.image.load('sources/sprites/key_points/sep_point.png')
        self.free_sprite = pygame.image.load('sources/sprites/key_points/free_point.png')
        self.image = self.free_sprite
        self.rect = self.image.get_rect()
        self.rect.x = 4 * 64 + 32
        self.rect.y = 4 * 64 + 32

    def change_side(self, side=None):
        if side == RES:
            self.image = self.res_sprite
        elif side == SEP:
            self.image = self.sep_sprite
        else:
            self.image = self.free_sprite
