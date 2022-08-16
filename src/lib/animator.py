import pygame
from .spritesheet import * 

class Animator(object):
    def __init__(self, filename, rect, count, key, loop, frames=1):
        self.filename = filename
        self.rect = rect
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(rect, count, key)
        self.i = 0
        self.loop = loop
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        if self.i >= len(self.iamges):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image
    
    def __add__(self, sheet):
        self.images.extend(sheet.images)
        return self
