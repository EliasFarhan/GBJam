import sys
from engine.const import log, render
from engine import const
if render == 'pygame':
	import pygame
elif render == 'sfml':
	import sfml
screen_size = (0,0)

def init_all():
	if render == 'pygame':
		pygame.init()
	init_screen()
	init_joystick()
def init_screen():
	global screen_size
	if render == 'pygame':
		pygame.mouse.set_visible(False)
		pygame.font.init()
		screen_size = const.screen_size
		return pygame.display.set_mode(screen_size,pygame.RESIZABLE)
	elif render == 'sfml':
		window = sfml.RenderWindow(sfml.VideoMode(const.screen_size[0],const.screen_size[1]),'SFML Window')
		return window
def init_joystick():
	pass
def get_screen_size():
	global screen_size
	return screen_size
def toogle_fullscreen():
	from engine.loop import get_screen,set_screen
	screen = get_screen()
	size = screen.get_size()
	flags = 0
	if screen.get_flags() == pygame.RESIZABLE:
		flags = pygame.FULLSCREEN | pygame.RESIZABLE
		screen_info = pygame.display.Info()
		size = (screen_info.current_w, screen_info.current_h)
	set_screen(pygame.display.set_mode(size,flags))
def resize_screen(w,h):
	from engine.loop import get_screen,set_screen
	screen = get_screen()
	size = (w,h)
	flags = screen.get_flags()
	set_screen(pygame.display.set_mode(size,flags))