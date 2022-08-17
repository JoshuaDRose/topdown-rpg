import os
import pygame
from .utils import *
from .animator import Animator as anim
from .spritesheet import *
from pygame.locals import *
from .consts import *

class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        spritesheet = load_sprite_sheet(r'src/sprites/world/entities/player/player.png')
        sheet_rect = spritesheet.get_rect()
        scaled = (sheet_rect.width * 3, sheet_rect.height * 3)
        self.spritesheet = pygame.transform.scale(spritesheet, scaled)
        self.idle = []
        self.walking = []
        self.walking_flipped = []

        # physics individual to the player
        self.vec = pygame.math.Vector2
        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)

        # The player will be scaled 3 times
        scale = 3
        key = (157, 142, 135)
        idle_positions = [
                (16, 16, 16, 16),
                (32, 16, 16, 16),
                (48, 16, 16, 16),
                (64, 16, 16, 16)
                ]
        walking_positions = [
                (16, 32, 16, 16),
                (32, 32, 16, 16),
                (48, 32, 16, 16),
                (64, 32, 16, 16)
                ]
        for n in idle_positions:
            scaled = (scale_normal(n, 3)[0], scale_normal(n, 3)[1], 16*3, 16*3)
            self.idle.append(image_at(self.spritesheet, scaled, key=key))
        for n in walking_positions:
            scaled = (scale_normal(n, 3)[0], scale_normal(n, 3)[1], 16 * 3, 16 * 3)
            image = image_at(self.spritesheet, scaled, key=key)
            self.walking.append(image)
            flipped = pygame.transform.flip(image, True, False)
            self.walking_flipped.append(flipped)

        self.n = 0
        self.tick = 0
        self.image = self.idle[self.n]
        self.flying = False
        self.gliding = False
        self.invincible = False
        self.drop = False # Is player falling through platforms?
        self.health: int = 20
        self.rect = pygame.Rect(position, (16, 16))

        self.vec = pygame.math.Vector2
        self.pos = self.vec((WIDTH / 2 - self.rect.width / 2, 385))



    def regulate_frames(self):
        if self.tick == 10:
            self.n += 1
            if self.n >= len(self.idle):
                self.n = 0
            self.image = self.idle[self.n]
            self.tick = 0
        self.tick += 1
        self.rect = self.idle[self.n].get_rect(topleft=self.pos)

    def jump(self):
        """
        collision = pygame.sprite.spritecollide(self, self.tiles, False)
        
        if collision:
            self.vel.y = -15
        """
        pass

    def update(self):
        """
        if not self.drop:
            # zcollision = pygame.sprite.spritecollide(self, tiles, False)
            if self.vel.y > 0:
                if collision:
                    self.pos.y = collision[0].rect.top + 1
                    self.vel.y = 0
        """

        self.acc = self.vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.acc.x = ACC
        if any((pressed_keys[K_UP], pressed_keys[K_SPACE], pressed_keys[K_w])):
            self.jump()

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        self.regulate_frames()
