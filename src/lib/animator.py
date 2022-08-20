""" Animator """
import pygame
from .spritesheet import *


class Animator:
    """ Animator class """
    def __init__(self, filename, rect, count, key, loop, frames=1):
        self.filename = filename
        self.rect = rect
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(rect, count, key)
        self.i = 0
        self.loop = loop
        self.f = frames
        self.frames = frames

    def iter(self):
        """ set frame iterators """
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        """ Goto next frame """
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image

    def __add__(self, sheet):
        """ Add surface to spritesheet """
        self.images.extend(sheet.images)
        return self
