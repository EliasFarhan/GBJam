from engine.scene import Scene
from engine.init import get_screen_size
from game_object.text import Text
from engine.const import framerate
from engine.sound_manager import snd_manager
from engine.image_manager import load_image, clear_screen, show_image
from game_object.image import Image
#font_obj, msg, sound_obj

class Kwakwa(Scene):
	def init(self):
		self.text = Image('data/sprites/text/kwakwa.png', 
						(get_screen_size()[0]/2,get_screen_size()[1]/2))
		self.count = 4*framerate
		snd_manager.play_music("data/sound/pissed_off_duck.wav")
		
	def loop(self, screen):
		clear_screen(255, 255, 255, screen)
		self.text.loop(screen, (0,0))
		if(not snd_manager.check_music_status()):
			import engine.level_manager as level_manager
			level_manager.switch_level(0)
