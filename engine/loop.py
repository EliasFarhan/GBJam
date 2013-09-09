import pygame, sys
import engine.init as init
import engine.level_manager as level_manager
from engine.event import loop as event_loop
from engine.event import init as event_init
from engine.event import end
from engine.const import framerate
finish = False
def loop(screen):
	global finish
	fps_clock = pygame.time.Clock()
	
	
	
	level_manager.switch("gameplay")
	
	while not finish:
		screen.fill(pygame.Color(0, 0, 0))
		
		event_loop()
		finish = end()
		f = level_manager.function_level()
		if f == 0:
			break
		else:
			f(screen)
			
		
		pygame.display.update()
		fps_clock.tick(framerate)
	pygame.quit()
	sys.exit()

def start():
	pygame.init()
	init.init_joystick()
	event_init()
	screen = init.init_screen()
	loop(screen)
	
	
