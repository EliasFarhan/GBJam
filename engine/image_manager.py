import pygame

class ImageManager():
	def __init__(self):
		self.images = {}
		self.index = 1
		self.img_name = {}
	
	def load(self, name):
		try:
			self.img_name[name]
		except KeyError:
			self.images[self.index] = pygame.image.load(name)
			self.img_name[name] = self.index
			self.index += 1
			return self.index - 1
		return self.img_name[name]
	
	def load_with_size(self, name, size):
		try:
			self.img_name[name]
		except KeyError:
			img = pygame.image.load(name)
			self.images[self.index] = pygame.transform.scale(img, size)
			self.img_name[name] = self.index
			self.index += 1
			return self.index - 1
		return self.img_name[name]
	
	def show(self, index, screen, pos,angle=0):
		if index == 0:
			return
		try:
			image_rect_obj = self.images[index].get_rect()
			image_rect_obj.center = (screen.get_rect().center[0]+pos[0], screen.get_rect().center[1]-pos[1])
			#rotation
			img = self.images[index]
			if angle != 0:
				img = pygame.transform.rotate(img,angle)
			screen.blit(img, image_rect_obj)
		except KeyError:
			pass
img_manager = ImageManager()