"""
Main loop of the engine
"""

from engine.const import CONST,log
import sys
from engine.physics import deinit_physics
from levels.loading_screen import LoadingScreen
from levels.logo_kwakwa import Kwakwa

if CONST.render == 'sfml':
    import sfml

from engine.init import init_all
import engine.level_manager as level_manager
from event.event_main import update_event, add_button, get_button
from levels.gamestate import GameState

finish = False
screen = None


def set_screen(new_screen):
    global screen
    screen = new_screen


def get_screen():
    global screen
    return screen


def set_finish():
    global finish
    finish = True


def loop():
    global finish, screen, console

    add_button('quit', ['ESC','LCTRL+q'])
    add_button('reset', ['r'])

    if CONST.debug:
        level_manager.switch_level(GameState(CONST.startup))
    else:
        level_manager.switch_level(Kwakwa())

    while not finish:
        update_event()
        if not finish:
            finish = get_button('quit')
        f = level_manager.update_level()
        if f == 0:
            log("No scene loaded",1)
            break
        else:
            f(screen)

        if get_button('reset'):
            level_manager.switch_level(GameState(CONST.startup))

        if CONST.render == 'sfml':
            screen.framerate_limit = CONST.framerate
            screen.display()
    deinit_physics()
    if CONST.render == 'sfml':
        screen.close()


def start():
    global screen
    log("START")
    screen = init_all()
    loop()
