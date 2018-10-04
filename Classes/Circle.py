import pygame

class Circle:
	def __init__(self, position, radius, width, color):
		self.position = position
		self.radius = radius
		self.width = width
		self.color = color

	def move(self, position):
		self.position = position

	def draw_on_display(self, display):
		pygame.draw.circle(display, self.color, self.position, self.radius, self.width)
