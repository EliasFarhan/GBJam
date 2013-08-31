import pygame

class ImageManager():
	def __init__(self):
		self.images = {}
	
	def load(self, name):
		try:
			self.images[name]
		except KeyError:
			self.images[name] = pygame.image.load(name)
	
	def load_with_size(self, name, size):
		try:
			self.images[name]
		except KeyError:
			img = pygame.image.load(name)
			self.images[name] = pygame.transform.scale(img, size)
	
	def show(self, name, screen, pos):
		
		try:
			image_rect_obj = self.images[name].get_rect()
			image_rect_obj.center = (screen.get_rect().center[0]+pos[0], screen.get_rect().center[1]-pos[1])
			screen.blit(self.images[name], image_rect_obj)
		except KeyError:
			pass
img_manager = ImageManager()