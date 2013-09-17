import pygame
from PIL import Image
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
			if pygame.image.get_extended():
				self.images[self.index] = pygame.image.load(name)
			else:
				self.images[self.index] = Image.open(name)
				self.images[self.index] = pygame.image.fromstring(self.images[self.index].tostring(), self.images[self.index].size, self.images[self.index].mode)
			self.images[self.index] = self.images[self.index].convert_alpha() 
			self.images[self.index] = self.images[self.index]
			self.img_name[name] = self.index
			self.index += 1
			return self.index - 1
		return self.img_name[name]
	
	def load_with_size(self, name, size):
		try:
			self.img_name[name]
		except KeyError:
			index = self.load(name)
			self.images[index] = pygame.transform.scale(self.images[index], size)
			self.img_name[name] = index
			return index
		return self.img_name[name]
	def load_big_image(self,name,size,nmb_block):
		pass
	def show(self, index, screen, pos,angle=0,rot_func=None,factor=1):
		if index == 0:
			return
		try:
			image = self.images[index]
			image_rect_obj = image.get_rect()
			if(factor != 1):
				image = pygame.transform.scale(image,(int(image_rect_obj.w*factor),int(image_rect_obj.h*factor)))
			image_rect_obj = image.get_rect()
			image_rect_obj.center = (screen.get_rect().center[0]+pos[0], screen.get_rect().center[1]-pos[1])
			if angle != 0 and rot_func != None:
				image,image_rect_obj = rot_func(image, image_rect_obj, angle)
			if(image_rect_obj.colliderect(screen.get_rect())):
				screen.blit(image, image_rect_obj)
		except KeyError:
			pass

img_manager = ImageManager()
