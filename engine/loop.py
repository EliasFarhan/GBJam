from engine.const import framerate, log, pookoo
import sys
if not pookoo:
	import pygame
else:
	import draw
	import window
import engine.init as init
import engine.level_manager as level_manager
from engine.event import update_event, add_button, get_button
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

def loop():
	global finish,screen,console
	if not pookoo:
		fps_clock = pygame.time.Clock()
		console = Console(screen, (0,0,init.get_screen_size()[0],init.get_screen_size()[1]/3))
	
	add_button('quit','ESC')
	
	level_manager.switch_level(GameState('data/json/level.json'))
	state = None
	state = draw.state_new()
	while not finish:
		if not pookoo:
			screen.fill(pygame.Color(0, 0, 0))
		
			console.process_input()
		else:
			draw.clear()
			draw.rgb(0.0, 0.0, 0.0)
			draw.rectangle(window.width(), window.height())
		update_event()
		finish = get_button('quit')
		f = level_manager.function_level()
		if f == 0:
			break
		else:
			f(screen)
		
		
		if not pookoo:
			console.draw()
			pygame.display.flip()
			fps_clock.tick(framerate)
	if not pookoo:
		pygame.quit()
	sys.exit()

def start():
	global fps,screen
	if not pookoo:
		pygame.init()
	screen = init.init_screen()
	loop()
	
	
