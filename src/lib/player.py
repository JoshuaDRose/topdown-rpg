""" player.py """
import os
import time
import pygame

from pygame.locals import *

import lib

from .animator import Animator as anim
from .spritesheet import *
from .consts import *
from .utils import *
from .timer import Timer


class Player(pygame.sprite.Sprite):
    """ Player class controllable by user """
    def __init__(self, position, groups):
        super().__init__(groups)
        spritesheet = load_sprite_sheet(r'sprites/world/tileset/gfx/character.png')
        sheet_rect = spritesheet.get_rect()
        scaled = (sheet_rect.width * 3, sheet_rect.height * 3)

        self.spritesheet = pygame.transform.scale(spritesheet, scaled)
        self.animation   = []
        self.walking     = [[], [], [], [], []]
        self.idle        = [[], [], [], [], []]
        self.slashing    = [[], [], [], [], []]

        self.player_tick            = lib.debug.Text((0, 0))
        self.player_state           = lib.debug.Text((0, 20))
        self.player_velocity        = lib.debug.Text((0, 40))
        self.player_position        = lib.debug.Text((0, 60))
        self.player_attack_tick     = lib.debug.Text((0, 80))
        self.player_acceleration    = lib.debug.Text((0, 100))
        self.player_attack_cooldown = lib.debug.Text((0, 120))

        self.vec = pygame.math.Vector2
        self.vel = self.vec(0, 0)
        self.acc = self.vec(0, 0)

        self.state = 0
        self.do_movement = False

        self.default_maxvel = MAXVEL
        self.current_maxvel = self.default_maxvel

        self.timers = {
            "sword": Timer(350, self.attack)
        }

        self.slash_animation = [
            # idle
            [
            (0, 128, 32, 32)
            ],
            # forward
            [
            (0, 128, 32, 32),
            (32, 128, 32, 32),
            (64, 128, 32, 32),
            (96, 128, 32, 32)
            ],
            # back
            [
            (0, 192, 32, 32),
            (32, 192, 32, 32),
            (64, 192, 32, 32),
            (96, 192, 32, 32)
            ],
            # right
            [
            (0, 160, 32, 32),
            (32, 160, 32, 32),
            (64, 160, 32, 32),
            (96, 160, 32, 32)
            ],
            # left
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

        for index, _ in enumerate(self.walking_positions):
            # pylint: disable=C0103
            for n in self.walking_positions[index]:
                scaled = (scale_normal(n, 3)[0], scale_normal(n, 3)[1], n[2] * 3, n[3] * 3)
                image = image_at(self.spritesheet, scaled)
                self.walking[index].append(image)
            self.idle[index].append(self.walking_positions[index][0])

        for index, _ in enumerate(self.slash_animation):
            # pylint: disable=C0103
            for n in self.slash_animation[index]:
                scaled = (scale_normal(n, 3)[0], scale_normal(n, 3)[1], n[2] * 3, n[3] * 3)
                image = image_at(self.spritesheet, scaled)
                self.slashing[index].append(image)

        # pylint: disable=C0103
        self.n = 0
        self.tick = 0
        self.image = self.walking[self.state][self.n]
        self.rect = pygame.Rect(position, (16, 16))
        self.pos = self.vec((WIDTH / 2 - self.rect.width / 2, 385))
        self.temp_pos = self.vec(self.pos)

        # pylint: disable=C0103
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.stop = False

        self.attacking = False
        self.holding_attack = False
        self.change_before = False
        self.change_after  = False
        self.origin_pos = self.vec(self.pos.x, self.pos.y)
        self.offset_x = 300
        self.attack_cooldown = 0

    def draw_debug(self):
        """ Draw debug overlay """
        self.player_tick.draw_text('player tick', self.tick)
        self.player_state.draw_text('player state', self.state)
        self.player_velocity.draw_text('speed', f'{round(self.vel.x, 1)} {round(self.vel.y, 1)}')
        self.player_position.draw_text('position', f'{round(self.pos.x, 2)} {round(self.pos.y, 2)}')
        self.player_attack_tick.draw_text('attack', self.attacking)
        self.player_acceleration.draw_text('accel', f'{round(self.acc.x, 3)} {round(self.acc.y, 1)}')
        self.player_attack_cooldown.draw_text('cooldown', f'{self.attack_cooldown}')

    def attack(self):
        """ Swing sword """
        if self.attacking:
            if self.attack_cooldown == 0:
                if self.state == 0:
                    self.state = 1
                if self.tick == 10:
                    self.n += 1
                    if self.n >= len(self.slashing[self.state]):
                        self.attacking = False
                        self.attack_cooldown = 50
                        self.n = 0
                        self.tick = 0
                    else:
                        self.image = self.slashing[self.state][self.n]
                    self.tick = 0
                self.tick += 1
                # self.rect = self.image.get_rect()
        else:
            self.tick = 0

    def regulate_frames(self):
        """ Statute the player frame rate to a set interavl """
        if not self.attacking:
            if self.tick == 10:
                # THIS COODE IS PROBLEMATIC
                """
                if self.attack:
                    self.n = 0
                    if self.n >= len(self.slashing[self.state]):
                        self.attack = False
                    self.image = self.slashing[self.state][self.n]
                    self.n += 1
                """
                if self.stop:
                    self.image = self.walking[self.state][0]
                else:
                    self.n += 1
                    if self.n >= len(self.walking[self.state]):
                        self.n = 0
                    self.image = self.walking[self.state][self.n]
                self.tick = 0
            self.tick += 1
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            # if self.attacking:
            #     self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y / 2))
            # else:
            #     self.rect = self.image.get_rect(center=(self.pos.x / 2, self.pos.y / 2))

    def reset_movement(self):
        """ Reset player movement """
        self.vel.x = 0
        self.vel.y = 0
        self.acc.x = 0
        self.acc.y = 0

    def update(self):
        """ Update vectors and animation """
        self.acc = self.vec(0, 0)
        if self.vel.magnitude() > 0:
            self.vel = self.vel.normalize()

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            if not self.attacking:
                self.state = 4
            self.acc.x = -ACC
            self.left = True
        else:
            self.left = False
            self.acc.x = max(self.acc.x, 0)

        if pressed_keys[K_RIGHT]:
            if not self.attacking:
                self.state = 2
            self.acc.x = ACC
            self.right = True
        else:
            self.right = False
            self.acc.x = min(self.acc.x, 0)

        if pressed_keys[K_UP]:
            if not self.attacking:
                self.state = 3
            self.acc.y = -ACC
            self.up = True
        else:
            self.up = False
            self.acc.y = max(self.acc.y, 0)

        if pressed_keys[K_DOWN]:
            if not self.attacking:
                self.state = 1
            self.acc.y = ACC
            self.down = True
        else:
            self.down = False
            self.acc.x = min(self.acc.y, 0)

        if pressed_keys[K_c]:
            # Cannot move and attack simultaneously
            if not self.attacking:
                if not self.holding_attack:
                    self.n = 0
                    self.attacking = True
        else:
            self.holding_attack = False

        if self.acc.x == 0 and self.acc.y == 0:
            self.stop = True
        else:
            self.stop = False

        moving = any((self.left, self.up, self.down, self.right))

        if self.attacking:
            moving = False
            if self.change_before:
                self.attack()
            else:
                self.n = 0
                self.reset_movement()
                self.change_before = True
        else:
            self.animation = self.walking_positions[self.state]

        if not moving:
            self.reset_movement()
        else:
            self.do_movement = 1

        if self.do_movement:
            if abs(self.acc.x) < self.current_maxvel:
                self.acc.x += round(self.vel.x * FRIC, 7)

            if abs(self.acc.y) < self.current_maxvel:
                self.acc.y += round(self.vel.y * FRIC, 7)
            self.vel += self.acc

            self.pos.x += self.vel.x + 0.5 * self.acc.x
            self.rect.centerx = self.pos.x

            self.pos.y += self.vel.y + 0.5 * self.acc.y
        else:
            self.rect.centerx = self.pos.x
            self.rect.centery = self.pos.y

        self.regulate_frames()
        self.draw_debug()
