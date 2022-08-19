import pygame

class Text:
    pygame.font.init()
    debugs = []
    font = pygame.font.Font(None, 30)

    def __init__(self, position):
        self.screen = pygame.display.get_surface()
        a, b, c, d = position[0], position[1], 200,20
        self.surf = pygame.Surface((c, d), pygame.SRCALPHA)
        self.surf.set_alpha(200)
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = a, b

    def draw_text(self, title, desc):
        txt = Text.font.render(f'{title}: {desc}', True, (255, 255, 255))
        self.surf.fill((0,0,0))
        self.surf.blit(txt, (0, 0))
        self.screen.blit(self.surf, self.rect)