from engine.const import pookoo
if not pookoo:
	import pygame
else:
	pass
from math import radians,cos,sin


images = {}
index = 1
img_name = {}
permanent_indexes = []

def draw_rect(screen,screen_pos,rect, color,angle=0):
	surface = pygame.Surface(rect.size,flags=pygame.SRCALPHA)
	surface.fill(pygame.Color(color[0],color[1],color[2],color[3]))
	
	rot_image, rot_rect = rot_center(surface, rect, angle)
	screen.blit(rot_image, (rot_rect[0]-screen_pos[0],rot_rect[1]-screen_pos[1]))
	
def fill_surface(surface,r,g,b,a=255):
	if(a==255):
		surface.fill((r,g,b))
	else:
		surface.fill((r,g,b,a))
def sanitize_img_manager():
	global images,permanent_indexes
	for index in images.keys():
		if index not in permanent_indexes:
			try:
				images.pop(index)
			except KeyError:
				pass
	
def get_image(index):
	global images
	return images[index]
def load_image(name,permanent=False):
	global images,permanent_indexes,index
	try:
		img_name[name]
	except KeyError:
		images[index] = pygame.image.load(name)
		images[index] = images[index].convert_alpha() 
		images[index] = images[index]
		img_name[name] = index
		index += 1
		if permanent:
			permanent_indexes.append(index-1)
		return index - 1
	return img_name[name]
	
def load_image_with_size(name, size,permanent=False):
	global img_name
	try:
		img_name[name]
	except KeyError:
		index = load_image(name,permanent)
		images[index] = pygame.transform.scale(images[index], size)
		img_name[name] = index
		return index
	return img_name[name]

def show_image(index, screen, pos,angle=0,center=False,rot_func=None,factor=1):
	if index == 0:
		return
	try:
		image = images[index]
		image_rect_obj = image.get_rect()
		if(factor != 1):
			image = pygame.transform.scale(image,(int(image_rect_obj.w*factor),int(image_rect_obj.h*factor)))
		image_rect_obj = image.get_rect()
		
		if center:
			image_rect_obj.center = (screen.get_rect().center[0]+int(pos[0]), screen.get_rect().center[1]-int(pos[1]))
		else:
			image_rect_obj.center = (int(pos[0]), int(pos[1]))
			
		if angle != 0:
			if rot_func == None:
				image,image_rect_obj = rot_center(image, image_rect_obj, angle)
			else:
				image,image_rect_obj = rot_func(image, image_rect_obj, angle)
		if(image_rect_obj.colliderect(screen.get_rect())):
			screen.blit(image, image_rect_obj)
	except KeyError:
		pass
	
def rot_center(image, rect, angle):
	"""rotate an image while keeping its center and size"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.get_center())
	return rot_image, rot_rect

