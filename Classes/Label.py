from ResourceManager import resource_manager
import pygame

class Label:
	def __init__(self, position, text, color):
		self.surface = resource_manager.get_font("monospace").render(text, 1, color)
		self.position = self.surface.get_rect(center = (position))

	def move(self, position):
		self.position = self.surface.get_rect(center = (position))

	def draw_on_display(self, display):
		display.blit(self.surface, self.position)