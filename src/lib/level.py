import pygame
from .tile import *
from .player import Player
from .settings import *

black = pygame.Color('black')
white = pygame.Color('white')


class Level:
    def __init__(self):
        if not pygame.display.get_init():
            pygame.display.init()
        else:
            print("Level Class: display already initialized")

        self.display_surface = pygame.display.get_surface()
        self.sprites_visible = pygame.sprite.Group()
        self.sprites_obstacle = pygame.sprite.Group()

        self.draw_map()


    def draw_map(self):
        # To ensure player is blitted last (on the top), save placeholder vars
        player_position: tuple = ()
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    # Grass((x, y), [self.sprites_visible])
                    pass
                if col == 'p':
                    player_position = (x, y)
                if col == 'd':
                    # Dirt((x, y), [self.sprites_visible])
                    pass
        Player(player_position, [self.sprites_visible])

    def run(self):
        """ Main level loop """
        self.display_surface.fill(white)
        self.sprites_visible.update()
        self.sprites_visible.draw(self.display_surface)


