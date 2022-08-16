import os
import pygame
from .utils import *
from .animator import Animator as anim
from .spritesheet import *
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.position = position
        spritesheet = load_sprite_sheet(r'src/sprites/world/entities/player/player.png')
        sheet_rect = spritesheet.get_rect()
        scaled = (sheet_rect.width * 3, sheet_rect.height * 3)
        self.spritesheet = pygame.transform.scale(spritesheet, scaled)
        self.idle = []
        # The player will be scaled 3 times
        scale = 3
        key = (157, 152, 135)
        idle_positions = [
                (16, 16, 16, 16),
                (32, 16, 16, 16),
                (48, 16, 16, 16),
                (64, 16, 16, 16)
                ]
        for n in idle_positions:
            scaled = (scale_normal(n, 3)[0], scale_normal(n, 3)[1], 16*3, 16*3)
            self.idle.append(image_at(self.spritesheet, scaled, key))
        self.n = 0
        self.tick = 0
        self.image = self.idle[self.n]
        self.flying = False
        self.gliding = False
        self.invincible = False
        self.health: int = 20
        self.rect = pygame.Rect(position, (16, 16))

    def regulate_frames(self):
        if self.tick == 10:
            self.n += 1
            if self.n >= len(self.idle):
                self.n = 0
            self.image = self.idle[self.n]
            print(self.image)
            self.tick = 0
        self.tick += 1
        self.rect = self.idle[self.n].get_rect(topleft=self.position)

    def update(self):
        self.regulate_frames()
