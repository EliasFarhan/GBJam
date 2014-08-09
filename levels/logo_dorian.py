# font_obj, msg, sound_obj
from engine.init import engine
from engine.rect import Rect
from engine.vector import Vector2
from game_object.image import Image
from levels.scene import Scene
from levels.title_screen import TitleScreen
from render_engine.img_manager import img_manager
from render_engine.snd_manager import snd_manager


class Dorian(Scene):
    def init(self):
        self.text = Image(path='data/sprites/text/logo-dorian_sred-2b_gameboy.png',
                          pos=Vector2(0,16),
                          size=Vector2(160, 128))
        self.text.init_image()
        snd_manager.set_playlist(['data/sound/logo_dorian_8bit.ogg'])
        self.screen_pos = Vector2()
    def loop(self, screen):
        img_manager.draw_rect(screen, Vector2(), Rect(Vector2(0, 0), engine.get_screen_size()), (255, 255, 255))
        self.text.loop(screen, False)

        if snd_manager.get_music_status():
            from engine.level_manager import switch_level

            switch_level(TitleScreen())
        snd_manager.update_music_status()

