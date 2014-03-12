'''
Main loop of the engine
'''

from engine.const import framerate, log, startup, render, debug
import sys
if render == 'pygame':
	import pygame
elif render == 'sfml':
	import sfml

import engine.init as init
import engine.level_manager as level_manager
from event.event_main import update_event
from event.keyboard_event import add_button, get_button
from levels.logo_kwakwa import Kwakwa
from engine.pyconsole import Console
from levels.gamestate import GameState

finish = False
screen = None
console = None

def get_console():
	global console
	return console

def set_screen(new_screen):
	global screen
	screen=new_screen
def get_screen():
	global screen
	return screen

def set_finish():
	global finish
	finish = True
	
def loop():
	global finish,screen,console
	if render == 'pygame':
		fps_clock = pygame.time.Clock()
		console = Console(screen, (0,0,init.get_screen_size()[0],init.get_screen_size()[1]/3))
	
	add_button('quit','ESC')
	add_button('reset','r')
	
	level_manager.switch_level(GameState(startup))
	
	while not finish:
		if render == 'pygame':
			screen.fill(pygame.Color(0, 0, 0))
			console.process_input()
		update_event()
		if not finish:
			finish = get_button('quit')
		f = level_manager.function_level()
		if f == 0:
			break
		else:
			f(screen)
			
		
		if get_button('reset'):
			level_manager.switch_level(GameState(startup))
		
		if render == 'pygame':
			console.draw()
			pygame.display.flip()
			fps_clock.tick(framerate)
		elif render == 'sfml':
			screen.vertical_synchronization = True
			screen.framerate_limit = framerate
	if render == 'pygame':
		pygame.quit()

def start():
	global fps,screen
	if render == 'pygame':
		pygame.init()
	screen = init.init_screen()
	loop()
	
	
