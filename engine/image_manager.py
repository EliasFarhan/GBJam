import pygame

class ImageManager():
	def __init__(self):
		self.images = {}
	
	def load(self, name):
		self.images[name] = pygame.image.load(name)
		
	def show(self, name, screen, pos):
		try:
			image_rect_obj = self.images[name].get_rect()
			image_rect_obj.center = pos
			screen.blit(self.images[name], image_rect_obj)
		except KeyError:
			pass
img_manager = ImageManager()