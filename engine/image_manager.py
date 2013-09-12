import pygame
from math import radians,cos,sin

def rot_center(image, rect, angle):
	"""rotate an image while keeping its center and size"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.center)
	return rot_image, rot_rect
def rot_electricity(img, rect,angle):
	new_img = pygame.transform.rotate(img,angle)
	if(angle %360 < 90 and angle%360 >= 0):
		new_bottomleft = (rect.bottomleft[0]-16*sin(radians(angle%360)),rect.bottomleft[1]-16*sin(radians(angle%360)))
		new_rect = new_img.get_rect(bottomleft=new_bottomleft)
	elif(angle%360 <180 and angle%360>= 90):
		rect.bottomright = rect.bottomleft
		new_bottomright = (rect.bottomright[0]+16*sin(radians(angle%360)),rect.bottomright[1]-16*sin(radians(angle%360)))
		new_rect = new_img.get_rect(bottomright=new_bottomright)
	elif(angle%360 <270 and angle%360 >=180):
		rect.topright = rect.topleft
		new_topright = (rect.topright[0]-16*sin(radians(angle%360)),rect.topright[1]-16*sin(radians(angle%360)))
		new_rect = new_img.get_rect(topright=new_topright)
	elif(angle%360 <360 and angle%360 >=270):
		new_topleft = (rect.topleft[0]+16*sin(radians(angle%360)),rect.topleft[1]-16*sin(radians(angle%360)))
		new_rect = new_img.get_rect(topleft=new_topleft)
	return new_img,new_rect
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
	
	def show(self, index, screen, pos,angle=0,rot_func=None,factor=1):
		if index == 0:
			return
		try:
			image = self.images[index]
			image_rect_obj = image.get_rect()
			if(factor != 1):
				image = pygame.transform.scale(image,(image_rect_obj.w*factor,image_rect_obj.h*factor))
			image_rect_obj = image.get_rect()
			image_rect_obj.center = (screen.get_rect().center[0]+pos[0], screen.get_rect().center[1]-pos[1])
			if angle != 0 and rot_func != None:
				image,image_rect_obj = rot_func(image, image_rect_obj, angle)
			screen.blit(image, image_rect_obj)
		except KeyError:
			pass

img_manager = ImageManager()
