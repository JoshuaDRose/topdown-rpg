import pygame
from .tile import *
from .player import Player
from .settings import *

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.sprites_visible = pygame.sprite.Group()
        self.sprites_obstacle = pygame.sprite.Group()

        self.draw_map()

    def draw_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Grass((x, y), [self.sprites_visible])
                if col == 'p':
                    Player((x, y), [self.sprites_visible])
                if col == 'd':
                    Dirt((x, y), [self.sprites_visible])

    def run(self):
        """ Main level loop """
        self.display_surface.fill(pygame.Color('black'))
        self.sprites_visible.update()
        self.sprites_visible.draw(self.display_surface)


