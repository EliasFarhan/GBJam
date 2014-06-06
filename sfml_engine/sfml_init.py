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
        #hide the sides
        first_rect = sfml.RectangleShape()
        first_rect.position = (0,0)
        second_rect = sfml.RectangleShape()
        if self.get_origin_pos().y > self.get_origin_pos().x:
            first_rect.size = (self.real_screen_size.x,self.get_origin_pos().y)
            second_rect.position = (0,self.real_screen_size.y-self.get_origin_pos().y)
            second_rect.size = first_rect.size
        else:
            first_rect.size = (self.get_origin_pos().x,self.real_screen_size.y)
            second_rect.position = (self.real_screen_size.x-self.get_origin_pos().x,0)
            second_rect.size = first_rect.size
        first_rect.fill_color = sfml.Color.BLACK
        second_rect.fill_color = sfml.Color.BLACK
        self.screen.draw(first_rect)
        self.screen.draw(second_rect)


        self.screen.framerate_limit = CONST.framerate
        self.screen.display()

    def get_origin_pos(self):
        origin_pos = Vector2()
        if self.real_screen_size.get_ratio() > self.screen_size.get_ratio():

            origin_pos = Vector2((self.real_screen_size.x -
                                 self.real_screen_size.y *
                                 self.real_screen_size.get_ratio())/2,0)
        else:
            origin_pos = Vector2(0,(self.real_screen_size.y -
                                   self.real_screen_size.x /
                                   self.screen_size.get_ratio())/2)
        return origin_pos

    def get_ratio(self):
        screen_diff_ratio = Vector2()
        if self.real_screen_size.get_ratio() > self.screen_size.get_ratio():
            screen_diff_ratio = self.screen_diff_ratio.y

        else:
            screen_diff_ratio = self.screen_diff_ratio.x
        return screen_diff_ratio