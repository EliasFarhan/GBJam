
from engine.const import log, CONST
from engine.level_manager import get_level

from engine.vector import Vector2
from json_export.json_main import load_json
from event.event_main import add_button

if CONST.render == 'sfml':
    import sfml
elif CONST.render == 'pookoo':
    import pookoo
elif CONST.render == 'kivy':
    import kivy
    from kivy.lang import Builder
    from kivy.app import App
    from kivy.uix.widget import Widget
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.uix.floatlayout import FloatLayout
    from input.keyboard_input import _on_keyboard_down

    class KuduGame(FloatLayout):
        def update(self, delta_time):
            get_level().loop(self)

        def __init__(self,**kwargs):
            super(KuduGame, self).__init__(**kwargs)
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=_on_keyboard_down)

        def _keyboard_closed(self):
            self._keyboard.unbind(on_key_down=_on_keyboard_down)
            self._keyboard = None

    class KuduApp(App):
        def build(self):
            game = KuduGame()
            Clock.schedule_interval(game.update, 1.0 / 60.0)
            return game


def init_all():
    screen = init_screen()
    if CONST.render == 'sfml':
        log(str(screen.settings))
    init_joystick()
    init_actions()
    return screen


def init_actions():
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


def init_screen():
    screen_size = CONST.screen_size
    log("Init screen with screen_size:" + str(screen_size))
    if CONST.render == 'sfml':
        desktop = sfml.VideoMode.get_desktop_mode()
        style = sfml.Style.DEFAULT
        if CONST.fullscreen:
            style = sfml.Style.FULLSCREEN
        window = sfml.RenderWindow(desktop, 'Kudu Window', style)
        return window
    elif CONST.render == 'pookoo':
        return pookoo.window.begin()
    elif CONST.render == 'kivy':
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

