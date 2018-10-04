import pygame
from collections import deque
import random

import Node
import MathFunctions as MF

class Canvas(pygame.Rect):
	def __init__(self, position, sizes):
		pygame.Rect.__init__(self, position, sizes)
		self.color = pygame.Color(41, 45, 54)

		self.nodes = []
		self.next_label = 1
		self.deleted_label = []
		self.edges = set()
		self.state = "idle"

	def mouse_down_move_graph(self, position):
		for node in self.nodes:
			if MF.distance(position, node.circle.position) <= node.circle.radius:
				self.selected_node = node
				self.state = "move_graph"
				break

	def mouse_up_move_graph(self, position):
		self.state = "idle"

	def mouse_down_add_node(self, position):
		touching_node = False
		for node in self.nodes:
			if MF.distance(position, node.circle.position) <= node.circle.radius:
				touching_node = True
				break

		if touching_node == False:
			self.add_node(position)

	def mouse_down_add_edge(self, position):
		for node in self.nodes:
			if MF.distance(position, node.circle.position) <= node.circle.radius:
				self.selected_node = node
				self.state = "add_edge"
				break

	def mouse_up_add_edge(self, position):
		self.state = "idle"
		for node in self.nodes:
			if MF.distance(position, node.circle.position) <= node.circle.radius:
				self.add_edge(self.selected_node, node)
				break

	def mouse_down_remove(self, position):
		for node in self.nodes:
			if MF.distance(position, node.circle.position) <= node.circle.radius:
				self.remove_node(node)
				break

	def update(self, position):
		if self.state == "move_graph":
			self.selected_node.move(position, [self.x, self.y], [self.width, self.height])
		elif self.state == "add_edge":
			touching_node = False
			for node in self.nodes:
				if MF.distance(position, node.circle.position) <= node.circle.radius:
					self.last_pos = node.get_position()
					touching_node = True
					break
			if touching_node == False:
				self.last_pos = position


	def draw_on_display(self, display):
		pygame.draw.rect(display, self.color, self)
		if self.state == "add_edge":
			pygame.draw.line(display, pygame.Color("white"), self.selected_node.get_position(), self.last_pos, 3)
		for edge in self.edges:
			pygame.draw.line(display, pygame.Color("white"), edge[0].get_position(), edge[1].get_position(), 3)
		for node in self.nodes:
			node.draw_on_display(display)

	def add_node(self, position, number = -1):
		if number != -1:
			self.nodes.append(Node.Node(position = position, text = str(number)))
		elif self.deleted_label:
			min_label = min(self.deleted_label)
			self.deleted_label.remove(min_label)
			self.nodes.append(Node.Node(position = position, text = str(min_label)))
		else:
			self.nodes.append(Node.Node(position = position, text = str(self.next_label)))
			self.next_label += 1
		return self.nodes[-1]


	def remove_node(self, node):
		self.edges = set(filter(lambda edge : node != edge[0] and node != edge[1], self.edges))
		self.deleted_label.append(node.number)
		self.nodes.remove(node)
			
	def add_edge(self, node_A, node_B):
		if node_A != node_B:
			self.edges.add((node_A, node_B))

	def get_graph(self):
		no_nodes = 0
		for edge in self.edges:
			no_nodes = max(no_nodes, edge[0].number, edge[1].number)
		for node in self.nodes:
			no_nodes = max(no_nodes, node.number)
		no_edges = len(self.edges)
		edges = []
		for edge in self.edges:
			edges.append([edge[0].number, edge[1].number])
		return no_nodes, no_edges, edges

	def save_graph(self):
		output_file = open("graph-text.txt", "w")
		no_nodes, no_edges, edges = self.get_graph()
		output_file.write(str(no_nodes) + ' ' + str(no_edges) + '\n')
		for edge in edges:
			output_file.write(str(edge[0]) + ' ' + str(edge[1]) + '\n') 

	def color_node(self, number, color):
		for node in self.nodes:
			if node.number == number:
				node.set_color(color)
				break

	def reset_graph(self):
		self.nodes = []
		self.edges = set()
		self.deleted_label = []
		self.next_label = 1

	def reset_nodes(self):
		for node in self.nodes:
			node.set_color(pygame.Color(41, 45, 54))

	def load_graph(self):
		self.reset_graph()
		input_file = open("graph-text.txt", "r").readlines()
		no_nodes, no_edges = list(map(int, input_file[0].split()))
		self.next_label = no_nodes + 1
		for line in input_file[1:]:
			no_A, no_B = list(map(int, line.split()))
			node_A, node_B = -1, -1
			for node in self.nodes:
				if node.number == no_A:
					node_A = node
				elif node.number == no_B:
					node_B = node
			if node_A == -1:
				position = [random.randint(self.x, self.x + self.width), random.randint(self.y, self.y + self.height)]
				node_A = self.add_node(position, no_A)
			if node_B == -1:
				position = [random.randint(self.x, self.x + self.width), random.randint(self.y, self.y + self.height)]
				node_B = self.add_node(position, no_B)
			self.edges.add((node_A, node_B))

	def set_state(self, state):
		self.state = state

	def delete_current_select(self):
		if self.state == "move_graph":
			self.remove_node(self.selected_node)
		self.state = "idle"
