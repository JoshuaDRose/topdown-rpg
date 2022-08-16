import os
import pygame
from .animator import Animator as anim
from .spritesheet import SpriteSheet as ss
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.spritesheet = ss('src/sprites/world/entities/player/player.png')
        self.idle: list = []
        self.idle = ss.images_at((16, 16, 16, 16), (64, 16, 79, 31), key=(157, 142, 135))
        self.n = 0
        self.tick = 0
        self.image = self.idle[self.n]

    def update(self):
        print(self.idle)
        if self.tick == 10:
            n += 1
            if n >= len(self.idle):
                n = 0
            self.image = self.idle[n]
            self.tick = 0
        self.tick += 1

