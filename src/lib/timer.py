""" Timer """
import pygame

class Timer:
    """ Timer """
    def __init__(self, duration, func=None):
        self.duration = duration
        self.st = 0
        self.active = False
        self.func = func

    def activate(self):
        """ Activate timer """
        self.active = True
        self.st = pygame.time.get_ticks()

    def deactivate(self):
        """ Deactivate timer """
        self.active = False
        self.st = 0

    def update(self):
        """ Update timer """
        current_time = pygame.time.get_ticks()
        if current_time - self.st >= self.duration:
            self.deactivate()
            if self.func:
                self.func()
