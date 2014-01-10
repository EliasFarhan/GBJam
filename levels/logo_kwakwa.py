from engine.scene import Scene
from engine.init import get_screen_size
from game_object.text import Text
import pygame
from engine.const import framerate
from engine.sound_manager import snd_manager
import math
from engine.image_manager import load_image
#font_obj, msg, sound_obj

class Kwakwa(Scene):
	def init(self):
		self.text = load_image('data/sprites/text/kwakwa.png')
		self.count = 4*framerate
		snd_manager.play_music("data/sound/pissed_off_duck.wav")
		
	def loop(self, screen):
		self.img_manager.clear_screen(255, 255, 255, screen)
		self.img_manager.show(self.text, screen, (get_screen_size()[0]/2, get_screen_size()[1]/2))

		
			
		if(not snd_manager.check_music_status()):
			import engine.level_manager as level_manager
			level_manager.switch_level(0)
