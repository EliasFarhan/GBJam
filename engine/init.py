import pygame, sys

screen_size = (0,0)
def init_screen():
	global screen_size
	screen_info = pygame.display.Info()
	screen_size = (screen_info.current_w, screen_info.current_h)
	print "Screen size: "+str(screen_size)
	pygame.mouse.set_visible(False)
	return pygame.display.set_mode(screen_size, pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
def init_joystick():
	pygame.joystick.init()
def get_screen_size():
	global screen_size
	return screen_size

