import pygame


if not pygame.display.init():
    print("Initializing pygame display from utils")
    pygame.display.init()

def scale_normal(size, factor):
    return (size[0] * factor, size[1] * factor)

def scale_sprite(sprite, factor) -> tuple:
    """
        Description: Scale a sprite by a given size
        sprite: pygame.Surface
        factor: integer
    """
    sprite = pygame.image.load(sprite).convert()
    rect = sprite.get_rect()
    size = (rect.width, rect.height)
    new_size = (size[0] * factor, size[1] * factor)
    return new_size
