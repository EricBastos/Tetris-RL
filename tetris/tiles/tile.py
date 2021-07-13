from abc import ABC, abstractmethod
import pygame
import os


class Tile(ABC, pygame.sprite.Sprite):

    def __init__(self, tile_img, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.abspath(tile_img))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, position):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def change_tile(self, new_image):
        self.image = pygame.image.load(os.path.abspath(new_image))
