import Circle
import Label
import pygame

class Node:
	def __init__(self, position, text):
		self.inner_circle = Circle.Circle(position = position, radius = 20, width = 0, color = pygame.Color(41, 45, 54))
		self.circle = Circle.Circle(position = position, radius = 20, width = 2, color = pygame.Color("white"))
		self.label = Label.Label(position = position, text = text, color = pygame.Color("white"))
		self.number = int(text)

	def move(self, position, canvas_position, canvas_size):
		for i in range(0, 2):
			if position[i] - self.circle.radius < canvas_position[i]:
				position[i] = canvas_position[i] + self.circle.radius
			elif position[i] + self.circle.radius > canvas_position[i] + canvas_size[i]:
				position[i] = canvas_position[i] + canvas_size[i] - self.circle.radius
		self.inner_circle.move(position)
		self.circle.move(position)
		self.label.move(position)

	def set_color(self, color):
		self.inner_circle.color = color

	def get_position(self):
		return self.circle.position

	def draw_on_display(self, display):
		self.inner_circle.draw_on_display(display)
		self.circle.draw_on_display(display)
		self.label.draw_on_display(display)