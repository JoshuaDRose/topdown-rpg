import os
import pygame
import time
import lib
from .animator import Animator as anim
from .spritesheet import *
from pygame.locals import *
from .consts import *
from .utils import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        spritesheet = load_sprite_sheet(r'sprites/world/tileset/gfx/character.png')
        sheet_rect = spritesheet.get_rect()
        scaled = (sheet_rect.width * 3, sheet_rect.height * 3)
        self.spritesheet = pygame.transform.scale(spritesheet, scaled)
        self.animation = []
        self.walking = [[],[],[],[],[]]
        self.walking_flipped = [[],[],[],[],[]]
        self.idle = [[],[],[],[],[]]
        self.slashing = [[],[],[],[],[]]

        self.player_tick = lib.debug.Text((0, 0))
        self.player_state = lib.debug.Text((0, 20))
        self.player_velocity = lib.debug.Text((0, 40))
        self.player_acceleration = lib.debug.Text((0, 60))

        slash_cooldown_timer = 200

        vec = self.vec = pygame.math.Vector2
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.change_dir = False
        self.state = 0
        self.do_movement = False
        self.attack = False

        scale = 1
        self.default_maxvel = MAXVEL
        self.current_maxvel = self.default_maxvel
        self.vel_cooldown = 0

        # x y width height
        self.slash_animation = [
            [
            (0, 128, 32, 32),
            (32, 128, 32, 32),
            (64, 128, 32, 32),
            (96, 128, 32, 32)
            ],
            [
            (0, 160, 32, 32),
            (32, 160, 32, 32),
            (64, 160, 32, 32),
            (11, 160, 32, 32)
            ],
            [
            (11, 192, 32, 32),
            (32, 192, 32, 32),
            (64, 192, 32, 32),
            (96, 192, 32, 32)
            ],
            [
            (0, 224, 32, 32),
            (32, 224, 32, 32),
            (64, 224, 32, 32),
            (96, 224, 32, 32)]]

        self.walking_positions = [
            # idle
            [
            (0, 0, 16, 32),
            ],
            # forward
            [
            (0, 0, 16, 32),
            (16, 0, 16, 32),
            (32, 0, 16, 32),
            (48, 0, 16, 32),
            ],
            # right
            [
            (0, 32, 16, 32),
            (16, 32, 16, 32),
            (32, 32, 16, 32),
            (48, 32, 16, 32),
            ],
            # back
            [
            (0, 64, 16, 32),
            (16, 64, 16, 32),
            (32, 64, 16, 32),
            (48, 64, 16, 32),
            ],
            # left
            [
            (0, 96, 16, 32),
            (16, 96, 16, 32),
            (32, 96, 16, 32),
            (48, 96, 16, 32),]]

        for index, array in enumerate(self.walking_positions):
            for n in self.walking_positions[index]:
                scaled = (scale_normal(n, 3)[0], scale_normal(n, 3)[1], n[2]*3, n[3]*3)
                image = image_at(self.spritesheet, scaled)
                self.walking[index].append(image)
            self.idle[index].append(self.walking_positions[index][0])

        for index, array in enumerate(self.slash_animation):
            for n in self.slash_animation[index]:
                scaled = (scale_normal(n, 3)[0], scale_normal(n, 3)[1], n[2]*3, n[3]*3)
                image = image_at(self.spritesheet, scaled)
                self.slashing[index].append(image)

        self.n = 0
        self.tick = 0
        self.image = self.walking[self.state][self.n]
        self.invincible = False
        self.health: int = 20
        self.rect = pygame.Rect(position, (16, 16))
        self.previous_rect = self.rect
        self.pos = vec((WIDTH / 2 - self.rect.width / 2, 385))
        self.diagonal = False

        # keys being pressed
        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.stop = False
        self.cooling = False
        self.n = 50


    def regulate_frames(self):
        """ Statute the player frame rate to a set interavl """
        self.player_tick.draw_text('player tick', self.tick)
        self.player_state.draw_text('player state', self.state)
        self.player_velocity.draw_text('speed', f'{round(self.vel.x, 1)} {round(self.vel.y, 1)}')
        self.player_acceleration.draw_text('accel', f'{round(self.acc.x, 3)} {round(self.acc.y, 1)}')
        if self.tick == 10:
            if self.attack:
                self.n = 0
                if self.n >= len(self.slashing[self.state]):
                    self.attack = False
                self.image = self.slashing[self.state][self.n]
                self.n += 1
            elif self.stop:
                self.image = self.walking[self.state][0]
            else:
                self.n += 1
                if self.n >= len(self.walking[self.state]):
                    self.n = 0
                self.image = self.walking[self.state][self.n]
            self.tick = 0
        self.tick += 1
        self.rect = self.image.get_rect(center=(self.pos.x/2, self.pos.y/2))


    def update(self):
        """ Update vectors and animation """
        self.acc = self.vec(0, 0)
        if self.vel.magnitude() > 0:
            self.vel = self.vel.normalize()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.state = 4
            self.acc.x = -ACC
            self.left = True
        else:
            self.left = False
            if self.acc.x < 0:
                self.acc.x = 0

        if pressed_keys[K_RIGHT]:
            self.state = 2
            self.acc.x = ACC
            self.right = True
        else:
            self.right = False
            if self.acc.x > 0:
                self.acc.x = 0

        if pressed_keys[K_UP]:
            self.state = 3
            self.acc.y = -ACC
            self.up = True
        else:
            self.up = False
            if self.acc.y < 0:
                self.acc.y = 0

        if pressed_keys[K_DOWN]:
            self.state = 1
            self.acc.y = ACC
            self.down = True
        else:
            self.down = False
            if self.acc.y > 0:
                self.acc.y = 0

        if pressed_keys[K_c]:
            """ NOTE: Cannot move and attack simultaneously """
            self.attack = True

        if self.acc.x == 0 and self.acc.y == 0:
            self.stop = True
        else:
            self.stop = False

        moving = any((self.left, self.up, self.down, self.right))
        self.animation = self.walking_positions[self.state]

        if abs(self.acc.x) < self.current_maxvel:
            self.acc.x += round(self.vel.x * FRIC, 7)
        if abs(self.acc.y) < self.current_maxvel:
            self.acc.y += round(self.vel.y * FRIC, 7)


        if not moving:
            self.vel.x = 0
            self.vel.y = 0
            self.acc.x = 0
            self.acc.y = 0

        if moving:
            if not self.attack:
                self.do_movement = True
            else:
                self.vel.x = 0
                self.vel.y = 0
                self.acc.x = 0
                self.acc.y = 0

        if self.do_movement:
            self.vel += self.acc

            self.pos.x += self.vel.x + 0.5 * self.acc.x
            self.rect.centerx = self.pos.x

            self.pos.y += self.vel.y + 0.5 * self.acc.y
            self.rect.centery = self.pos.y

        self.regulate_frames()
