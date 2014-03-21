
import sys
from engine.const import log, render, fullscreen
from engine import const
from engine.vector import Vector2
if render == 'pygame':
	import pygame
elif render == 'sfml':
	import sfml
screen_size = (0,0)

def init_all():
	if render == 'pygame':
		pygame.init()
	screen = init_screen()
	if render == 'sfml':
		log(str(screen.settings))
	init_joystick()
	return screen
def init_screen():
	global screen_size
	screen_size = const.screen_size
	if render == 'pygame':
		pygame.mouse.set_visible(False)
		pygame.font.init()
		
		return pygame.display.set_mode(screen_size,pygame.RESIZABLE)
	elif render == 'sfml':
		desktop = sfml.VideoMode.get_desktop_mode()
		style = sfml.Style.DEFAULT
		if fullscreen:
			style = sfml.Style.FULLSCREEN
		window = sfml.RenderWindow(desktop,'Kudu Window',style)
		return window
def init_joystick():
	pass
def get_screen_size():
	global screen_size
	return Vector2().coordinate(screen_size[0],screen_size[1])
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