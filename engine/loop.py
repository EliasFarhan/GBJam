import pygame, sys
import engine.init as init
import engine.level_manager as level_manager
from engine.event import update_event
from engine.event import init as event_init
from engine.event import is_end
from engine.const import framerate,startup
from levels.logo_kwakwa import Kwakwa

finish = False
fps = None
screen = None

def set_screen(new_screen):
	global screen
	screen=new_screen
def get_screen():
	global screen
	return screen

def loop():
	global finish,fps,screen
	fps_clock = pygame.time.Clock()
	
	
	
	level_manager.switch_level(Kwakwa())
	
	while not finish:
		screen.fill(pygame.Color(0, 0, 0))
		
		update_event()
		finish = is_end()
		f = level_manager.function_level()
		if f == 0:
			break
		else:
			f(screen)
		msg_surface_obj = fps.render(str(int(fps_clock.get_fps())), False, pygame.Color(0,0,0))
		msg_rect_obj = msg_surface_obj.get_rect()
		msg_rect_obj.topleft = (0, 0)
		screen.blit(msg_surface_obj, msg_rect_obj)
	#	pygame.display.update()
		pygame.display.flip()
		fps_clock.tick(framerate)
	pygame.quit()
	sys.exit()

def start():
	global fps,screen
	pygame.init()
	fps = pygame.font.Font('data/font/8-BITWONDER.ttf',25)
	init.init_joystick()
	event_init()
	screen = init.init_screen()
	loop()
	
	
