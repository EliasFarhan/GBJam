import sfml
from engine.const import CONST
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