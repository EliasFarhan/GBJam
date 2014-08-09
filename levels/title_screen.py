import sfml
from engine.const import CONST
from engine.init import engine
from engine.rect import Rect
from engine.vector import Vector2
from game_object.image import Image
from game_object.text import Text
from levels.gamestate import GameState
from levels.scene import Scene
from render_engine.img_manager import img_manager
from render_engine.input import input_manager
from render_engine.snd_manager import snd_manager

__author__ = 'Elias'

class TitleScreen(Scene):
    def init(self):
        snd_manager.set_playlist(['data/music/menu_gbjam.ogg'])
        self.img = img_manager.load_image("data/sprites/text/Title.png")
        self.font = sfml.Font.from_file("data/font/SILKWONDER.ttf")
        self.text = sfml.Text("PRESS START", self.font, 14)
        self.text.position = (50,130)
        self.text.color = sfml.Color.BLACK
        self.screen_pos = Vector2()
        self.time = 0
    def loop(self, screen):
        img_manager.draw_rect(screen, Vector2(), Rect(Vector2(0, 0), engine.get_screen_size()), (255, 255, 255))
        img_manager.show_image(self.img,screen,Vector2())
        if (self.time % 20) > 10:
            img_manager.buffer.draw(self.text)

        self.time += 1
        if input_manager.get_button("A") or input_manager.get_button("B"):
            from engine.level_manager import switch_level
            switch_level(GameState(CONST.startup))
        snd_manager.update_music_status()