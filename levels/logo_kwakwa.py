from engine.vector import Vector2
from levels.loading_screen import LoadingScreen
from levels.scene import Scene
from engine.init import get_screen_size
from engine.const import CONST
from engine.img_manager import fill_surface
from game_object.image import Image
from engine.snd_manager import play_music, check_music_status
from levels.gamestate import GameState
#font_obj, msg, sound_obj


class Kwakwa(Scene):
    def init(self):
        self.loading_screen = LoadingScreen()
        self.loading_screen.init_method = [GameState(CONST.startup)]
        self.loading_screen.init()
        self.text = Image('data/sprites/text/kwakwa.png',
                          get_screen_size()/2)
        self.text.pos = self.text.pos-self.text.size/2
        self.count = 4 * CONST.framerate
        play_music("data/sound/pissed_off_duck.wav")

    def loop(self, screen):
        fill_surface(screen, 255, 255, 255)
        self.text.loop(screen, Vector2())
        if check_music_status():
            from engine.level_manager import switch_level
            switch_level(self.loading_screen)


