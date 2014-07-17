from engine.rect import Rect
from engine.vector import Vector2
from levels.loading_screen import LoadingScreen
from levels.scene import Scene
from engine.init import engine
from engine.const import CONST
from game_object.image import Image
from levels.gamestate import GameState
#font_obj, msg, sound_obj
from render_engine import img_manager, snd_manager


class Kwakwa(Scene):
    def init(self):
        self.loading_screen = LoadingScreen()
        self.loading_screen.init_method = [GameState(CONST.startup)]
        self.loading_screen.init()
        self.text = Image('data/sprites/text/kwakwa.png',
                          engine.get_screen_size()/2)
        self.text.pos = self.text.pos-self.text.size/2
        self.count = 4 * CONST.framerate
        snd_manager.play_music("data/sound/pissed_off_duck.wav")

    def loop(self, screen):
        img_manager.draw_rect(screen,Vector2(),Rect(Vector2(0,0),engine.get_screen_size()),(255,255,255))
        self.text.loop(screen, Vector2())
        if snd_manager.check_music_status():
            from engine.level_manager import switch_level
            switch_level(self.loading_screen)


