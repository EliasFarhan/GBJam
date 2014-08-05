from engine.rect import Rect
from engine.vector import Vector2
from levels.loading_screen import LoadingScreen
from levels.scene import Scene
from engine.init import engine
from engine.const import CONST, log
from game_object.image import Image
from levels.gamestate import GameState
#font_obj, msg, sound_obj
from render_engine.img_manager import img_manager
from render_engine.snd_manager import snd_manager


class Kwakwa(Scene):
    def init(self):
        #self.loading_screen = LoadingScreen()
        #self.loading_screen.init_method = [GameState(CONST.startup)]
        #self.loading_screen.init()
        self.text = Image(path='data/sprites/text/kwakwa_logo.png',
                          pos=Vector2(),
                          size=Vector2(160,144))
        self.text.init_image()
        self.count = 4 * CONST.framerate
        snd_manager.play_music("data/sound/pissed_off_duck.wav")
        self.screen_pos = Vector2()

    def loop(self, screen):
        log("WKAKWAKWA")
        img_manager.draw_rect(screen,Vector2(),Rect(Vector2(0,0),engine.get_screen_size()),(255,255,255))
        self.text.loop(screen)
        if snd_manager.get_music_status():
            from engine.level_manager import switch_level
            switch_level(GameState(CONST.startup))
        snd_manager.update_music_status()


