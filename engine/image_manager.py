'''
Manage images loading, transforming and rendering
'''
from engine.const import render, log


if render == 'pygame':
	import pygame
elif render == 'sfml':
	import sfml
	
from math import radians,cos,sin


images = {}
img_name = {}
permanent_images= []

def draw_rect(screen,screen_pos,rect, color,angle=0):
	if render == 'pygame':
		surface = pygame.Surface(rect.size,flags=pygame.SRCALPHA)
		surface.fill(pygame.Color(color[0],color[1],color[2],color[3]))
		
		rot_image, rot_rect = rot_center(surface, rect, angle)
		screen.blit(rot_image, (rot_rect[0]-screen_pos[0],rot_rect[1]-screen_pos[1]))

def fill_surface(surface,r,g,b,a=255):
	if render == 'pygame':
		if(a==255):
			surface.fill((r,g,b))
		else:
			surface.fill((r,g,b,a))
	elif render == 'sfml':
		surface.clear()
def sanitize_img_manager():
	for index in images.keys():
		if index not in permanent_images:
			try:
				images.pop(index)
			except KeyError:
				pass
	
def get_image(index):
	return images[index]

def get_size(index):
	if render == 'pygame':
		return index.get_size()
def load_image(name,permanent=False):
	try:
		img_name[name]
	except KeyError:
		if render == 'pygame':
			img_name[name] = pygame.image.load(name).convert_alpha()
		elif render == 'sfml':
			img_name[name] = sfml.Sprite(sfml.Texture.from_file(name))
		if permanent:
			permanent_images.append(name)
	return img_name[name]
	
def load_image_with_size(name, size,permanent=False):
	try:
		img_name[name]
	except KeyError:
		index = load_image(name,permanent)
		if size != None and render == 'pygame':
			img_name[name] = pygame.transform.scale(img_name[name], size)
	return img_name[name]

def show_image(image, screen, pos,angle=0,center=False,new_size=None,rot_func=None,factor=1,center_image=False):
	if image == 0:
		return
	try:
		if render == 'pygame':
			image_rect_obj = image.get_rect()
			if(factor != 1):
				image = pygame.transform.scale(image,(int(image_rect_obj.w*factor),int(image_rect_obj.h*factor)))
			if(new_size):
				image = pygame.transform.scale(image,new_size)
			image_rect_obj = image.get_rect()
			
			if center:
				image_rect_obj.center = (screen.get_rect().center[0]+int(pos[0]), screen.get_rect().center[1]-int(pos[1]))
			else:
				if center_image:
					image_rect_obj.center = (int(pos[0]), int(pos[1]))
				else:
					image_rect_obj.topleft = (int(pos[0]), int(pos[1]))
				
			if angle != 0:
				if rot_func == None:
					image,image_rect_obj = rot_center(image, image_rect_obj, angle)
				else:
					image,image_rect_obj = rot_func(image, image_rect_obj, angle)
			if(image_rect_obj.colliderect(screen.get_rect())):
				screen.blit(image, image_rect_obj)
		elif render == 'sfml':
			if new_size:
				text_size = image.texture.size
				
				image.ratio = sfml.Vector2(new_size[0]/float(text_size[0]),new_size[1]/float(text_size[1]))
			if angle!=0:

				image.rotation = angle
			image.position = pos
			screen.draw(image)
	except KeyError:
		pass
	
def rot_center(image, rect, angle):
	"""rotate an image while keeping its center and size"""
	rot_image = pygame.transform.rotate(image, angle)
	rot_rect = rot_image.get_rect(center=rect.get_center())
	return rot_image, rot_rect

