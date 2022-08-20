import pygame
from .utils import *

class Cursor:
	def __init__(self, position):
		""" Essential cursor params """
		path = r'sprites/ui/screen/cursor.png'
		sf = 2 # scale factor
		size = scale_sprite(path, sf)
		self.image = pygame.transform.scale(pygame.image.load(path).convert(), size)
		self.rect = self.image.get_rect(topleft=position)
		self.mousepos = position
		self.image.set_colorkey((0, 0, 0))
		pygame.mouse.visible = False
		print("mouse.visible=false")

	def update(self):
		""" Update cursor position """
		self.rect.x, self.rect.y = self.mousepos
		