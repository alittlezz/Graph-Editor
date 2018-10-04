import pygame

import Button

class SelectedOption(pygame.Rect):
	def __init__(self, rect, color):
		position = (rect.x, rect.y)
		sizes = (rect.width, rect.height)
		self.border_width = int(max(sizes) * 0.02)
		pygame.Rect.__init__(self, position, sizes)
		self.color = color
		self.activated = False

	def turn_on(self):
		self.activated = True

	def turn_off(self):
		self.activated = False

	def draw_on_display(self, display):
		pygame.draw.rect(display, self.color, self, self.border_width)

class Sidebar(pygame.Rect):
	def __init__(self, position, sizes):
		pygame.Rect.__init__(self, position, sizes)
		self.color = pygame.Color(55, 62, 72)

		self.buttons = []
		self.add_buttons(position, sizes)
		self.active_option = SelectedOption(self.buttons[0], pygame.Color(151, 44, 222))
		self.temporary_option = SelectedOption(self.buttons[-1], pygame.Color("blue"))
		#self.temporary_option.turn_off()

		self.duration = 0
		self.MAX_DURATION = 1
		
	def get_action(self, position):
		action = "idle"
		for button in self.buttons:
			if button.collidepoint(position) == True:
				action = button.get_action()
				break
		return action

	def draw_on_display(self, display):
		pygame.draw.rect(display, self.color, self)
		for button in self.buttons:
			button.draw_on_display(display)
		self.active_option.draw_on_display(display)
		if self.temporary_option.activated == True:
			self.temporary_option.draw_on_display(display)

	def set_temporary_option(self, action):
		for button in self.buttons:
			if button.get_action() == action:
				self.temporary_option = SelectedOption(button, pygame.Color("blue"))
				self.duration = self.MAX_DURATION
				self.temporary_option.turn_on()
				break

	def set_active_option(self, action):
		for button in self.buttons:
			if button.get_action() == action:
				self.active_option = SelectedOption(button, pygame.Color(151, 44, 222))
				break

	def update(self, delta):
		if self.temporary_option.activated == True:
			self.duration -= delta
			if self.duration < 0:
				self.duration = 0
				self.temporary_option.turn_off()


	def add_buttons(self, position, sizes):
		button_width = sizes[1] * 0.1
		button_space = button_width / 3
		button_size = [sizes[0] * 0.9, button_width]
		button_position = [position[0] + sizes[0] * 0.05, button_width / 2]
		self.buttons.append(Button.Button(position = button_position, sizes = button_size, text = "Move graph", action = "move_graph"))
		
		button_position[1] += button_width + button_space
		self.buttons.append(Button.Button(position = button_position, sizes = button_size, text = "Add node", action = "add_node"))

		button_position[1] += button_width + button_space
		self.buttons.append(Button.Button(position = button_position, sizes = button_size, text = "Add edge", action = "add_edge"))

		button_position[1] += button_width + button_space
		self.buttons.append(Button.Button(position = button_position, sizes = button_size, text = "Remove element", action = "remove"))

		button_position[1] += button_width + button_space
		self.buttons.append(Button.Button(position = button_position, sizes = button_size, text = "Play animation", action = "play_animation"))

		button_position[1] += button_width + button_space
		self.buttons.append(Button.Button(position = button_position, sizes = button_size, text = "Save graph", action = "save_graph"))

		button_position[1] += button_width + button_space
		self.buttons.append(Button.Button(position = button_position, sizes = button_size, text = "Load graph", action = "load_graph"))