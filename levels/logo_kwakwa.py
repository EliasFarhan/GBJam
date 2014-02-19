from levels.scene import Scene
from engine.init import get_screen_size
from engine.const import framerate
from engine.image_manager import fill_surface
from game_object.image import Image
from engine.sound_manager import play_music, check_music_status
from levels.gamestate import GameState
#font_obj, msg, sound_obj

class Kwakwa(Scene):
	def init(self):
		self.text = Image('data/sprites/text/kwakwa.png', 
						(get_screen_size()[0]/2,get_screen_size()[1]/2))
		self.count = 4*framerate
		play_music("data/sound/pissed_off_duck.wav")
		
	def loop(self, screen):
		fill_surface(screen,255, 255, 255)
		self.text.loop(screen, (0,0))
		if(not check_music_status()):
			from engine.level_manager import switch_level
			switch_level(GameState('data/json/level.json'))


			
