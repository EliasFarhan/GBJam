import pygame, init, sys
from pygame.locals import *
def loop(screen):
	fpsClock = pygame.time.Clock()
	screen.fill(pygame.Color(0, 0, 0))
	finish = False
	while not finish:
		pass
		for event in pygame.event.get():
			if event.type == QUIT:
				finish = True
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					finish = True
		pygame.display.update()
	pygame.quit()
	sys.exit()

def start():
	pygame.init()
	screen = init.init_screen()
	loop(screen)
	
