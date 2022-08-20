import pygame
from pygame.locals import *

import os
import sys
import glob

if not pygame.display.get_init():
    pygame.display.init()

def load_sprite_sheet(file) -> pygame.Surface:
    """ Load spritesheet as a surface """
    return pygame.image.load(file)

def image_at(sheet, rect, key=None) -> pygame.Surface:
    """
        Description: Load an image from rect
        rect: tuple | list
        key: bool | tuple
    """
    image_rect = pygame.Rect(rect)

    if key is not None:
        image = pygame.Surface(image_rect.size).convert()
        image.blit(sheet, (0, 0), image_rect)
        if key is -1:
            key = image.get_at((0, 0))
        image.set_colorkey(key, pygame.RLEACCEL)
    else:
        image = pygame.Surface(image_rect.size, pygame.SRCALPHA)
        image.set_colorkey((0,0,0))
        image.blit(sheet, (0, 0), image_rect)
    return image

def images_at(rects, key=None) -> list:
    """
        Description: Load multiple images from a list or tuple
        rects: list | tuple
        key: boolean | tuple
    """
    images = []

    for rect in rects:
        images.append(image_at(rect, key))

    return images


def load_strip(rect, image_count, key=None) -> list:
    """
        Description: Return list of sprites from strip
        image_count: integer
        key: boolean | tuple
    """
    tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
            for x in range(image_count)]
    return images_at(tups, key)
