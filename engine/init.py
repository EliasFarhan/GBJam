from engine import level_manager
from engine.const import log, CONST


from engine.vector import Vector2
from json_export.json_main import load_json
from event.event_main import add_button, get_button, update_event


class Engine():
    def __init__(self):
        self.screen = None
        self.finish = False

    def init_screen(self):
        self.screen_size = CONST.screen_size

    def init_joystick(self):
        pass

    def init_actions(self):
        actions = None

        if isinstance(CONST.actions, CONST.string_type):
            actions = load_json(CONST.actions)
        elif isinstance(CONST.actions, dict):
            actions = CONST.actions
        else:
            log("Error: could not load actions, Undefined type: "+str(type(CONST.actions)), 1)
            return
        for key in actions.items():
            log(key)
            add_button(key[0], key[1])

    def init_level(self):
        if not CONST.debug:
            from levels.logo_kwakwa import Kwakwa
            level_manager.switch_level(Kwakwa())

    def init_all(self):
        self.init_screen()
        self.init_joystick()
        self.init_actions()
        self.init_level()
        return self.screen

    def loop(self):
        add_button('quit', ['LCTRL+q'])
        add_button('reset', ['r'])
        while not self.finish:
            self.pre_update()
            update_event()

            self.finish = get_button('quit')

            f = level_manager.update_level()

            if f == 0:
                log("No scene loaded",1)
                break
            else:
                f(self.screen)
            if get_button('reset'):
                from levels.gamestate import GameState
                level_manager.switch_level(GameState(CONST.startup))
            self.post_update()

    def pre_update(self):
        pass

    def post_update(self):
        pass

    @staticmethod
    def get_screen_size():
        return Vector2(CONST.screen_size)

engine = Engine()

real_screen_size = Vector2()
kivy_screen = None
if CONST.render == 'sfml':
    from sfml_engine.sfml_init import SFMLEngine
    engine = SFMLEngine()
elif CONST.render == 'pookoo':
    import pookoo
elif CONST.render == 'kivy':
    """import kivy
    from kivy.app import App
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.config import Config
    from kivy.uix.widget import Widget
    from input.keyboard_input import _on_keyboard_down

    class KuduGame(Widget):

        def __init__(self,**kwargs):
            super(KuduGame, self).__init__(**kwargs)
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=_on_keyboard_down)

        def _keyboard_closed(self):
            self._keyboard.unbind(on_key_down=_on_keyboard_down)
            self._keyboard = None

        def update(self, delta_time):
            get_level().loop(self)

    class KuduApp(App):
        def build(self):
            # print the application informations
            log('\nKudu v%s  Copyright (C) 2014  Elias Farhan')

            from kivy.base import EventLoop
            EventLoop.ensure_window()
            self.window = EventLoop.window


            global real_screen_size, kivy_screen
            self.kudu_widget = KuduGame(app=self)
            self.root = self.kudu_widget

            kivy_screen = self.kudu_widget

            from engine.loop import init_level
            init_level()
            Clock.schedule_interval(self.kudu_widget.update, 1.0 / 60.0)
    """


'''
def init_all():
    global kivy_screen
    init_engine.init_screen()
    if CONST.render == 'sfml':
        log(str(screen.settings))
    init_joystick()
    init_actions()
    return init_engine.screen





def init_screen():
    screen_size = CONST.screen_size
    log("Init screen with screen_size:" + str(screen_size))
    if CONST.render == 'sfml':

        return window
    elif CONST.render == 'pookoo':
        return pookoo.window.begin()
    elif CONST.render == 'kivy':
        if CONST.fullscreen:
            Config.set('graphics', 'fullscreen', '0')
        Config.set('graphics', 'width', '1920')
        Config.set('graphics', 'height', '1080')
        Config.write()
        return KuduApp()


def init_joystick():
    pass


def get_screen_size(relative=False):
    if not relative:
        return Vector2(CONST.screen_size[0], CONST.screen_size[1])
    else:
        if CONST.render == 'pookoo':
            return Vector2(pookoo.window.size())


def toogle_fullscreen():
    """TODO: toggle fullscreen"""


def resize_screen(new_size):
    """TODO: resize window"""

def get_kivy_screen():
    global kivy_screen
    return kivy_screen
'''