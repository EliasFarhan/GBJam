from engine.level_manager import switch_level
from levels.gamestate import GameState

__author__ = 'efarhan'

from engine.const import CONST, log
from engine.image_manager import fill_surface
from engine.init import get_screen_size
from engine.vector import Vector2
from game_object.text import Text
from levels.scene import Scene
import copy

if CONST.render == 'sfml':
    import sfml


class LoadingScreen(Scene):
    def __init__(self):
        self.y_size = 100
        self.loading_text = Text(Vector2(get_screen_size().x/2, self.y_size/2),self.y_size,"data/font/pixel_arial.ttf","Loading",center=True,relative=True,color=(255,255,255))
        self.counter = 0
        self.anim_length = CONST.animation_step
        self.text_points = ""
        self.init_method = []

        if CONST.render == 'sfml':
            self.loading_thread = sfml.Thread(LoadingScreen.loading, self)
            self.loading_lock = sfml.Mutex()
            self.status = False

    def get_loading_state(self):
        status = False
        if CONST.render == 'sfml':
            self.loading_lock.lock()
            status = copy.deepcopy(self.status)
            self.loading_lock.unlock()

        return status

    def finish_loading(self):
        if CONST.render == 'sfml':
            self.loading_lock.lock()
            self.status = True
            self.loading_lock.unlock()

    def init(self):
        if CONST.render == 'sfml':
            try:
                self.loading_thread.launch()
            except RuntimeError:
                pass
        elif CONST.render == 'pookoo':
            self.loading()
            
    def loading(self):
        """Run init method in a different thread"""
        for scene in self.init_method:
            scene.init(loading=True)
        self.finish_loading()

    def loop(self, screen):
        if self.get_loading_state():
            switch_level(GameState(CONST.startup))
            return


        fill_surface(screen, 0, 0, 0)
        self.counter = (self.counter + 1) % self.anim_length
        if self.counter == 0:
            self.text_points += "."
            if self.text_points == '....':
                self.text_points = ""
            self.loading_text.set_text("Loading"+self.text_points)
        self.loading_text.loop(screen,Vector2())