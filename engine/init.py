import sys
from engine.const import log,pookoo
if not pookoo:
	import pygame
screen_size = (0,0)
def init_screen():
	global screen_size
	screen_info = pygame.display.Info()
	screen_size = (screen_info.current_w, screen_info.current_h)
	screen_size = (1280,720)
	log("Screen size: "+str(screen_size))
	pygame.mouse.set_visible(False)
	return pygame.display.set_mode(screen_size)
def init_joystick():
	pygame.joystick.init()
def get_screen_size():
	global screen_size
	return screen_size
def toogle_fullscreen():
	from engine.loop import get_screen,set_screen
	screen = get_screen()
	size = screen.get_size()
	flags = 0
	if screen.get_flags() == 0:
		flags = pygame.FULLSCREEN
		screen_info = pygame.display.Info()
		size = (screen_info.current_w, screen_info.current_h)
	set_screen(pygame.display.set_mode(size,flags))
	
