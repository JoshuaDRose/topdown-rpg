import pygame

pygame.font.init()

font = pygame.font.Font(None, 30)

# however many debug text is on screen
debugs = []


def debug(info):
    y = len(debugs) * 15
    x = 10
    screen = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, pygame.Color('white'))
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    pygame.draw.rect(screen, pygame.Color('black'), debug_rect)
    screen.blit(debug_surf, debug_rect)

