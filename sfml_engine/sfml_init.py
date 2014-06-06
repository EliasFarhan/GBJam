import sfml
from engine import level_manager
from engine.const import CONST, log

from engine.init import Engine
from engine.vector import Vector2

__author__ = 'Elias'


class SFMLEngine(Engine):
    def init_screen(self):
        desktop = sfml.VideoMode.get_desktop_mode()
        style = sfml.Style.DEFAULT
        if CONST.fullscreen:
            style = sfml.Style.FULLSCREEN
        self.screen = sfml.RenderWindow(desktop, 'Kudu Window', style)
        self.real_screen_size = Vector2(self.screen.size)
        self.screen_diff_ratio = self.real_screen_size/self.screen_size
        log(self.screen_size.get_tuple())
        log(self.real_screen_size.get_tuple())
        log(self.screen_diff_ratio.get_tuple())

    def init_level(self):
        from levels.loading_screen import LoadingScreen
        if CONST.debug:
            level_manager.switch_level(LoadingScreen())
        else:
            Engine.init_level(self)

    def pre_update(self):
        from engine.img_manager import img_manager
        img_manager.clear_screen(self.screen)

    def post_update(self):
        self.screen.framerate_limit = CONST.framerate
        self.screen.display()