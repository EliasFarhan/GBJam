from engine.const import framerate, log, pookoo
import sys
if not pookoo:
	import pygame
import engine.init as init
import engine.level_manager as level_manager
from engine.event import update_event, add_button, get_button
from levels.logo_kwakwa import Kwakwa
from engine.pyconsole import Console
from levels.gamestate import GameState

finish = False
fps = None
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
	global finish,fps,screen,console
	fps_clock = pygame.time.Clock()
	console = Console(screen, (0,0,screen.get_size()[0],screen.get_size()[1]/3))
	
	add_button('quit','ESC')
	
	level_manager.switch_level(GameState('data/json/level.json'))
	
	while not finish:
		screen.fill(pygame.Color(0, 0, 0))
		
		console.process_input()
		
		update_event()
		finish = get_button('quit')
		f = level_manager.function_level()
		if f == 0:
			break
		else:
			f(screen)
		msg_surface_obj = fps.render(str(int(fps_clock.get_fps())), False, pygame.Color(255,255,255))
		msg_rect_obj = msg_surface_obj.get_rect()
		msg_rect_obj.topleft = (0, 0)
		screen.blit(msg_surface_obj, msg_rect_obj)
		
		console.draw()
	#	pygame.display.update()
		pygame.display.flip()
		fps_clock.tick(framerate)
	pygame.quit()
	sys.exit()

def start():
	global fps,screen
	pygame.init()
	fps = pygame.font.Font('data/font/8-BITWONDER.ttf',25)
	screen = init.init_screen()
	loop()
	
	
