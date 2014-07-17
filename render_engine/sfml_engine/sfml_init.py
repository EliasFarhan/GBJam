import sfml

from engine import level_manager
from engine.const import CONST, log
from engine.init import Engine
from render_engine.input import input_manager
from engine.level_manager import get_level
from engine.vector import Vector2



__author__ = 'Elias'


class SFMLEngine(Engine):
    def init_screen(self):
        desktop = sfml.VideoMode.get_desktop_mode()
        if CONST.debug:
            desktop = sfml.VideoMode(800,600)
        style = sfml.Style.DEFAULT
        if CONST.fullscreen and not CONST.debug:
            style = sfml.Style.FULLSCREEN
        self.screen = sfml.RenderWindow(desktop, 'Kudu Window', style)
        self.real_screen_size = Vector2(self.screen.size)
        self.screen_diff_ratio = self.real_screen_size / self.screen_size

        input_manager.init()

    def init_level(self):
        from levels.loading_screen import LoadingScreen

        if CONST.debug:
            level_manager.switch_level(LoadingScreen())
        else:
            Engine.init_level(self)

    def pre_update(self):
        from render_engine.img_manager import img_manager
        img_manager.clear_screen(self.screen)

    def post_update(self):
        #hide the sides
        first_rect = sfml.RectangleShape()
        first_rect.position = (0, 0)
        second_rect = sfml.RectangleShape()
        if self.get_origin_pos().y > self.get_origin_pos().x:
            first_rect.size = (self.real_screen_size.x, self.get_origin_pos().y)
            second_rect.position = (0, self.real_screen_size.y - self.get_origin_pos().y)
            second_rect.size = first_rect.size
        else:
            first_rect.size = (self.get_origin_pos().x, self.real_screen_size.y)
            second_rect.position = (self.real_screen_size.x - self.get_origin_pos().x, 0)
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
                                  self.screen_size.get_ratio()) / 2, 0)
        else:
            origin_pos = Vector2(0, (self.real_screen_size.y -
                                     self.real_screen_size.x /
                                     self.screen_size.get_ratio()) / 2)
        return origin_pos

    def get_ratio(self):
        screen_diff_ratio = Vector2()
        if self.real_screen_size.get_ratio() > self.screen_size.get_ratio():
            screen_diff_ratio = self.screen_diff_ratio.y

        else:
            screen_diff_ratio = self.screen_diff_ratio.x
        return screen_diff_ratio

    def exit(self):

        from render_engine.img_manager import img_manager

        img_manager.sanitize_img_manager(remove_all=True)
        self.screen.close()
        Engine.exit(self)

    def update_event(self):
        """
        Update the states of Input Event
        """
        window = self.screen
        input_manager.update_joy_event()
        for event in window.events:
            input_manager.update_keyboard_event(event)

            if type(event) is sfml.CloseEvent:
                from engine.init import engine

                engine.finish = True
            elif type(event) is sfml.MouseButtonEvent:
                from engine.init import engine
                screen_ratio = float(engine.get_screen_size().y) / Vector2(engine.screen.size).y
                from levels.gamestate import GameState

                if get_level().__class__ == GameState:
                    log((Vector2(event.position) * screen_ratio + get_level().screen_pos).get_tuple())
            elif type(event) is sfml.ResizeEvent:
                new_size = event.size

