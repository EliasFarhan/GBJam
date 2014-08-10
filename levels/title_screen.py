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

class TitleScreen(Scene):
    def init(self):
        snd_manager.set_playlist(['data/music/menu_gbjam.ogg'])
        self.img = img_manager.load_image("data/sprites/text/Title.png")
        self.font = sfml.Font.from_file("data/font/SILKWONDER.ttf")
        self.text = sfml.Text("PRESS START", self.font, 10)
        self.text.position = (58,63)
        self.text.color = sfml.Color.BLACK
        self.screen_pos = Vector2()
        self.time = 0
        self.dialog = False

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
            img_manager.show_image(self.img,screen,Vector2(0,-48))


            if (self.time % 20) > 10:
                img_manager.buffer.draw(self.text)

            self.time += 1
        if not self.dialog and (input_manager.get_button("A") or input_manager.get_button("B")):
            snd_manager.set_playlist(["data/music/intro_BOSS1_gbjam.ogg","data/music/BOSS1_gbjam.ogg"])
            self.dialog = 1
            engine.show_dialog = True
            engine.textbox.set_text("Fury", "General Meow, you are still alive")
        if self.dialog == 1 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 2
                engine.textbox.set_text("General Meow", "I'm not easy to kill. Don't forget it")
        if self.dialog == 2 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 3
                engine.textbox.set_text("Fury","I won't miss you next time")
        if self.dialog == 3 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                engine.show_dialog = False
                from engine.level_manager import switch_level
                switch_level(GameState(CONST.startup))
        snd_manager.update_music_status()