import pygame

pygame.font.init()


def load_header(size):
    """ load font surface """
    return pygame.font.SysFont('Impact', size)

def h1(text, color) -> pygame.Surface:
    """ load header text """
    font = load_header(50)
    return font.render(text, True, color)
