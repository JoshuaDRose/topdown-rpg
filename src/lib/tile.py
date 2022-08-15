import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image: pygame.Surface = pygame.image.load('sprites/world/grass/1.png').convert()
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(topleft = position)
        self.position = position
        self.groups = groups
