from engine.scene import Scene
import pygame
#font_obj, msg, sound_obj

class Kwakwa(Scene):
	def init(self):
		self.font = pygame.font.Font("data/font/LittleSnorlax.ttf", 72)
		self.msg = u'KwaKwa'
		
		pygame.mixer.music.load("data/sound/pissed_off_duck.wav")
		pygame.mixer.music.play()
	def loop(self, screen):
		if pygame.mixer.music.get_busy():
			msg_surface_obj = self.font.render(self.msg, False, pygame.Color(255, 255, 255))
			msg_rect_obj = msg_surface_obj.get_rect()
			msg_rect_obj.center = (screen.get_size()[0]/2, screen.get_size()[1]/2)
			screen.blit(msg_surface_obj, msg_rect_obj)
		else:
			import engine.level_manager as level_manager
			level_manager.switch("logo_pygame")