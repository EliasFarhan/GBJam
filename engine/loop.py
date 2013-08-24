import pygame, sys
import engine.init as init
import engine.level_manager as level_manager
from pygame.locals import *

def loop(screen):
	fps_clock = pygame.time.Clock()
	
	finish = False
	
	level_manager.switch("logo_kwakwa")
	
	while not finish:
		screen.fill(pygame.Color(0, 0, 0))
		
		f = level_manager.function_level()
		if f == 0:
			break
		else:
			f(screen)
			
		for event in pygame.event.get():
			if event.type == QUIT:
				finish = True
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					finish = True
		pygame.display.update()
		fps_clock.tick(30)
	pygame.quit()
	sys.exit()

def start():
	pygame.init()
	screen = init.init_screen()
	loop(screen)
	
