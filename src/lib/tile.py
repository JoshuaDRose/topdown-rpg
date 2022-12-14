""" contains tile classes """
import random
import glob
import pygame


class Grass(pygame.sprite.Sprite):
    """ Grass tile class """
    def __init__(self, position, groups):
        """ Grass constructor """
        super().__init__(groups)
        tiles = []
        for i in glob.glob('sprites/world/grass/*'):
            tiles.append(pygame.image.load(i).convert())
        self.image    = random.choice(tiles)
        self.rect     = self.image.get_rect(topleft=position)
        self.position = position
        self.groups   = groups


class Dirt(pygame.sprite.Sprite):
    """ Dirt tile class """
    def __init__(self, position, groups):
        """ Dirt constructor """
        super().__init__(groups)
        self.image    = pygame.image.load('sprites/world/dirt/1.png').convert()
        self.rect     = self.image.get_rect(topleft=position)
        self.position = position
        self.groups   = groups
