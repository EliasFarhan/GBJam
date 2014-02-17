from engine.const import pookoo, log,path_prefix
if not pookoo:
	import pygame
else:
	import texture
	import draw
	
from math import radians,cos,sin


images = {}
img_name = {}
permanent_images= []

def draw_rect(screen,screen_pos,rect, color,angle=0):
	if not pookoo:
		surface = pygame.Surface(rect.size,flags=pygame.SRCALPHA)
		surface.fill(pygame.Color(color[0],color[1],color[2],color[3]))
		
		rot_image, rot_rect = rot_center(surface, rect, angle)
		screen.blit(rot_image, (rot_rect[0]-screen_pos[0],rot_rect[1]-screen_pos[1]))
	else:
		draw.state_save(screen)
		draw.rgb(color[0]/255,color[1]/255,color[2]/255)
		
		draw.translate(rect.pos[0]-screen_pos[0],rect.pos[1]-screen_pos[1])
		if angle != 0:
			draw.rotate(-angle)
		draw.rectangle(rect.size[0],rect.size[1])
		draw.state_restore(screen)
def fill_surface(surface,r,g,b,a=255):
	if not pookoo:
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

def get_size(index):
	global images
	if not pookoo:
		return index.get_size()
def load_image(name,permanent=False):
	global images,permanent_images
	try:
		img_name[name]
	except KeyError:
		if not pookoo:
			img_name[name] = pygame.image.load(name).convert_alpha()
		else:
			img_name[name] = texture.open(name)
		if permanent:
			permanent_images.append(name)
	return img_name[name]
	
def load_image_with_size(name, size,permanent=False):
	global img_name
	try:
		img_name[name]
	except KeyError:
		index = load_image(name,permanent)
		if size != None and not pookoo:
			img_name[name] = pygame.transform.scale(img_name[name], size)
	return img_name[name]

def show_image(image, screen, pos,angle=0,center=False,rot_func=None,factor=1):
	if image == 0:
		return
	try:
		if not pookoo:
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
		else:
			draw.state_save(screen)
			if factor != 1:
				draw.scale(factor)
			if center:
				draw.translate(window.width()/2+int(pos[0]),window.height/2-int(pos[1]))
			else:
				draw.translate(pos[0],pos[1])
			if angle != 0:
				draw.rotate(angle)
			
			draw.texture(image)
			draw.state_restore(screen)
	except KeyError:
		pass
	
def rot_center(image, rect, angle):
	"""rotate an image while keeping its center and size"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.get_center())
	return rot_image, rot_rect

