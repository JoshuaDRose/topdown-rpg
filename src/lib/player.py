import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        self.rect = self.surf.get_rect()