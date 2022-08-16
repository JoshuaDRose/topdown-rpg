import pygame
import random
import glob

class Grass(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        tiles = []
        for i in glob.glob('src/sprites/world/grass/*'):
            tiles.append(pygame.image.load(i).convert())
        # print(tiles)
        self.image = random.choice(tiles)
        self.rect = self.image.get_rect(topleft = position)
        self.position = position
        self.groups = groups

class Dirt(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load('src/sprites/world/dirt/1.png').convert()
        self.rect = self.image.get_rect(topleft = position)
        self.position = position
        self.groups = groups
