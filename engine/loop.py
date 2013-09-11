import pygame, sys
import engine.init as init
import engine.level_manager as level_manager
from engine.event import loop as event_loop
from engine.event import init as event_init
from engine.event import is_end
from engine.const import framerate,startup
finish = False
fps = None
def loop(screen):
	global finish,fps
	fps_clock = pygame.time.Clock()
	
	
	
	level_manager.switch(startup)
	
	while not finish:
		screen.fill(pygame.Color(0, 0, 0))
		
		event_loop()
		finish = is_end()
		f = level_manager.function_level()
		if f == 0:
			break
		else:
			f(screen)
		msg_surface_obj = fps.render(str(int(fps_clock.get_fps())), False, pygame.Color(255, 255, 255))
		msg_rect_obj = msg_surface_obj.get_rect()
		msg_rect_obj.topleft = (0, 0)
		screen.blit(msg_surface_obj, msg_rect_obj)
		pygame.display.update()
		fps_clock.tick(framerate)
	pygame.quit()
	sys.exit()

def start():
	global fps
	pygame.init()
	fps = pygame.font.Font('data/font/8-BITWONDER.ttf',25)
	init.init_joystick()
	event_init()
	screen = init.init_screen()
	loop(screen)
	
	
