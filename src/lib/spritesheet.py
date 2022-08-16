import pygame
from pygame.locals import *

import os
import sys
import glob


class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print(f"Unable to load spritesheet: {filename}")
            raise SystemExit

    def image_at(self, rect, key=None):
        """ Load image from rect """
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if key:
            if key is -1:
                key = image.get_at((0, 0))
            image.set_colorkey(key, pygame.RLEACCEL)
        return image

    def images_at(self, rects, key=None):
        """ Load multiple images from rect """
        return [self.image_at(rect, key) for rect in rects]

    def load_strip(self, rect, image_count, key=None):
        """ Load strip of sprites as list """
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, key)
