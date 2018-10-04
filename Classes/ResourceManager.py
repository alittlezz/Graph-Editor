import pygame

class ResourceManager:
	def __init__(self):
		pygame.init()

		self.fonts = {}
		self.load_fonts()

		self.textures = {}
		self.load_textures()

	def load_fonts(self):
		self.fonts["monospace"] = pygame.font.SysFont("monospace", 20)

	def get_font(self, name):
		return self.fonts[name]

	def load_textures(self):
		pass

resource_manager = ResourceManager()