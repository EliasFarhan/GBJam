import sys
from engine.const import log, CONST

from engine.vector import Vector2
from json_export.json_main import load_json
from event.event_main import add_button

if CONST.render == 'sfml':
    import sfml


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
    elif type(CONST.actions) == dict:
        actions = CONST.actions
    else:
        log("Error: could not load actions, Undefined type: "+str(type(CONST.actions)),1)
        return
    for key in actions.items():
        log(key)
        add_button(key[0], key[1])


def init_screen():
    screen_size = CONST.screen_size
    if CONST.render == 'sfml':
        desktop = sfml.VideoMode.get_desktop_mode()
        style = sfml.Style.DEFAULT
        if CONST.fullscreen:
            style = sfml.Style.FULLSCREEN
        window = sfml.RenderWindow(desktop, 'Kudu Window', style)
        return window


def init_joystick():
    pass


def get_screen_size():
    return Vector2(CONST.screen_size[0], CONST.screen_size[1])


def toogle_fullscreen():
    """TODO: toggle fullscreen"""


def resize_screen(w, h):
    """TODO: resize window"""