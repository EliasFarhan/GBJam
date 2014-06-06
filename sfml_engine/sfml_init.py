import sfml
from engine import level_manager
from engine.const import CONST
from engine.img_manager import img_manager
from engine.init import Engine

__author__ = 'Elias'


class SFMLEngine(Engine):
    def init_screen(self):
        Engine.init_screen(self)
        desktop = sfml.VideoMode.get_desktop_mode()
        style = sfml.Style.DEFAULT
        if CONST.fullscreen:
            style = sfml.Style.FULLSCREEN
        self.screen = sfml.RenderWindow(desktop, 'Kudu Window', style)

    def init_level(self):
        from levels.loading_screen import LoadingScreen
        if CONST.debug:
            level_manager.switch_level(LoadingScreen())
        else:
            Engine.init_level(self)

    def pre_update(self):
        img_manager.clear_screen(self.screen)

    def post_update(self):
        self.screen.framerate_limit = CONST.framerate
        self.screen.display()