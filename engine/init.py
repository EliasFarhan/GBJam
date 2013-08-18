import pygame

def init_screen():
	screen_info = pygame.display.Info()
	screen_size = (screen_info.current_w, screen_info.current_h)
	print "Screen size: "+str(screen_size)
	return pygame.display.set_mode(screen_size, pygame.FULLSCREEN)