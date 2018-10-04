import pygame
import Label

class Button(pygame.Rect):
	def __init__(self, position, sizes, text, action):
		pygame.Rect.__init__(self, position, sizes)
		self.color = pygame.Color(41, 45, 54)
		self.action = action
		self.label = Label.Label(position = [pos + size / 2 for pos, size in zip(position, sizes)], text = text, color = pygame.Color("white"))

	def draw_on_display(self, display):
		pygame.draw.rect(display, self.color, self)
		self.label.draw_on_display(display)

	def get_action(self):
		return self.action