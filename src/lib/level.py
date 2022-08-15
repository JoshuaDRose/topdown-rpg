import pygame

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.sprites_visible = pygame.sprite.Group()
        self.sprites_obstacle = pygame.sprite.Group()

    def run(self):
        pass



