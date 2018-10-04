import pygame
from collections import deque

import Canvas
import Sidebar
import algo

class Game:
	def __init__(self):
		pygame.init()
		self.FPS = 40
		self.is_running = True

		self.sizes = [1280, 720]
		self.background_color = pygame.Color("white")
		self.display = pygame.display.set_mode(self.sizes)
		pygame.display.set_caption("Graph editor")

		self.canvas = Canvas.Canvas(position = [200, 0], sizes = [1080, 720])
		self.sidebar = Sidebar.Sidebar(position = [0, 0], sizes = [200, 720])

		self.is_mouse_dragging = False
		self.state = "move_graph"

		self.frame_duration = 0.5
		self.frame_time = 0

		self.run()

	def mouse_down_canvas(self, position):
		if self.state == "move_graph":
			self.canvas.mouse_down_move_graph(position)
		elif self.state == "add_node":
			self.canvas.mouse_down_add_node(position)
		elif self.state == "add_edge":
			self.canvas.mouse_down_add_edge(position)
		elif self.state == "remove":
			self.canvas.mouse_down_remove(position)

	def mouse_up_canvas(self, position):
		if self.state == "move_graph":
			self.canvas.mouse_up_move_graph(position)
		elif self.state == "add_edge":
			self.canvas.mouse_up_add_edge(position)

	def handle_events_sidebar(self, position):
		action = self.sidebar.get_action(position)
		if action == "idle":
			return
		if action == "save_graph" or action == "load_graph":
			self.sidebar.set_temporary_option(action)
			if action == "save_graph":
				self.canvas.save_graph()
			elif action == "load_graph":
				self.canvas.load_graph()
				self.sidebar.set_active_option("move_graph")
				self.state = "movve_graph"
		else:
			self.state = action
			self.sidebar.set_active_option(action)
			if action == "play_animation":
				no_nodes, no_edges, edges = self.canvas.get_graph()
				self.animation_actions = algo.get_actions(no_nodes, no_edges, edges)
				if len(self.animation_actions) > 0:
					self.frame_time = self.frame_duration
				else:
					self.state = "move_graph"
					self.sidebar.set_active_option("move_graph")
					self.canvas.reset_nodes()

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if self.canvas.collidepoint(event.pos) == True:
					self.mouse_down_canvas(event.pos)
				elif self.sidebar.collidepoint(event.pos) == True:
					self.handle_events_sidebar(event.pos)
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				self.mouse_up_canvas(event.pos)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.exit()
				elif event.key == pygame.K_DELETE:
					self.canvas.delete_current_select()


	def draw(self):
		self.canvas.draw_on_display(self.display)
		self.sidebar.draw_on_display(self.display)

	def update(self, delta):
		delta /= 1000
		if self.state == "play_animation":
			self.frame_time -= delta
			if self.frame_time <= 0:
				self.frame_time = self.frame_duration
				number, color = self.animation_actions.popleft()
				self.canvas.color_node(number, pygame.Color(color))
				if not self.animation_actions:
					self.state = "move_graph"
					self.sidebar.set_active_option("move_graph")
					self.canvas.reset_nodes()

		self.sidebar.update(delta)
		self.canvas.update(list(pygame.mouse.get_pos()))

	def run(self):
		clock = pygame.time.Clock()
		while self.is_running:
			self.reset()
			self.handle_events()
			self.update(clock.tick(self.FPS))
			self.draw()
			pygame.display.update()

	def exit(self):
		self.is_running = False

	def reset(self):
		self.display.fill(self.background_color)