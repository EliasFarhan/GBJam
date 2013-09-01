import pygame, sys

def init_screen():
	screen_info = pygame.display.Info()
	screen_size = (screen_info.current_w, screen_info.current_h)
	print "Screen size: "+str(screen_size)
	if sys.platform != 'darwin':
                return pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
        else:
                return pygame.display.set_mode(screen_size)
