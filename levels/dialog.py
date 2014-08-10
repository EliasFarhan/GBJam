from engine import level_manager

__author__ = 'Elias'

import sfml
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

class Dialog(Scene):
    def init(self):

        self.font = sfml.Font.from_file("data/font/SILKWONDER.ttf")
        self.screen_pos = Vector2()
        self.time = 0
        self.player = Image(Vector2())

        self.dialog = False
        self.last_checkpoint = Vector2()
        self.cat = Image(Vector2(),path="data/sprites/text/CatPortrait.png",size=Vector2(79,74))
        self.cat.init_image(size=Vector2(79,74))
        self.cat.pos = engine.screen_size-self.cat.size
        self.ferret = Image(Vector2(),path="data/sprites/text/FerretPortrait.png",size=Vector2(73,74))
        self.ferret.init_image(size=Vector2(73,74))

        self.ferret.pos = Vector2(0,engine.screen_size.y)-Vector2(0,self.cat.size.y)

    def loop(self, screen):
        img_manager.draw_rect(screen, Vector2(), Rect(Vector2(0, 0), engine.get_screen_size()), (255, 255, 255))
        self.cat.loop(screen)
        self.ferret.loop(screen)
        if not self.dialog:
            snd_manager.set_playlist(["data/music/intro_BOSS1_gbjam.ogg","data/music/BOSS1_gbjam.ogg"])
            self.dialog = 1
            engine.show_dialog = True
            engine.textbox.set_text("Fury", "I'm coming for you, General Meow")
        if self.dialog == 1 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 3
                engine.textbox.set_text("General Meow", "I have a surprise for you, Fury")

        if self.dialog == 3 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                engine.show_dialog = False
                from levels.gamestate import GameState
                boss_level = GameState("data/json/boss_level.json")
                boss_level.last_checkpoint = self.last_checkpoint
                level_manager.switch_level(boss_level)
        snd_manager.update_music_status()