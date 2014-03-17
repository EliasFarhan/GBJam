'''
Main loop of the engine
'''

from engine.const import framerate, log, startup, render, debug
import sys
from engine.physics import deinit_physics
if render == 'pygame':
	import pygame
elif render == 'sfml':
	import sfml

from engine.init import init_all
import engine.level_manager as level_manager
from event.event_main import update_event
from event.keyboard_event import add_button, get_button
from levels.logo_kwakwa import Kwakwa
from levels.gamestate import GameState

finish = False
screen = None




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
	
	add_button('quit','ESC')
	add_button('reset','r')
	
	level_manager.switch_level(GameState(startup))
	
	while not finish:
		update_event()
		if not finish:
			finish = get_button('quit')
		f = level_manager.update_level()
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
			screen.framerate_limit = framerate
			screen.display()
	deinit_physics()
	if render == 'pygame':
		pygame.quit()

def start():
	global fps,screen
	
	screen = init_all()
	loop()
	
	
