from engine.const import log, CONST

from engine.vector import Vector2

if CONST.render == 'sfml':
    import sfml
screen_size = (0, 0)


def init_all():

    screen = init_screen()
    if CONST.render == 'sfml':
        log(str(screen.settings))
    init_joystick()
    return screen


def init_screen():
    global screen_size
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
    global screen_size
    return Vector2().coordinate(screen_size[0], screen_size[1])


def toggle_fullscreen():
    """TODO: toggle the screen to fullscreen or not"""


def resize_screen(w, h):
    """TODO: resize the given windows"""