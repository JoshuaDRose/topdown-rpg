import pygame

pygame.font.init()


def load_header(size):
    return pygame.font.SysFont('Impact', size)

def h1(text, color) -> pygame.Surface:
    font = load_header(50)
    return font.render(text, True, color)
