from engine.const import CONST
from engine.init import engine
from engine.rect import Rect
from engine.vector import Vector2
from game_object.image import Image
from levels.gamestate import GameState
from levels.scene import Scene
from render_engine.img_manager import img_manager
from render_engine.input import input_manager
from render_engine.snd_manager import snd_manager

__author__ = 'Elias'

class TitleScreen(Scene):
    def init(self):
        snd_manager.set_playlist(['data/music/menu_gbjam.ogg'])
        self.screen_pos = Vector2()

    def loop(self, screen):
        img_manager.draw_rect(screen, Vector2(), Rect(Vector2(0, 0), engine.get_screen_size()), (255, 255, 255))

        if input_manager.get_button("A") or input_manager.get_button("START"):
            from engine.level_manager import switch_level
            switch_level(GameState(CONST.startup))
        snd_manager.update_music_status()