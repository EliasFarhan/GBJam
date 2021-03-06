﻿"""
Main loop of the engine
"""

'''
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


def init_level():
    if CONST.debug:
        if CONST.render == 'sfml':
            level_manager.switch_level(LoadingScreen())
        elif CONST.render == 'pookoo' or CONST.render == 'kivy':
            level_manager.switch_level(GameState(CONST.startup))
    else:
        level_manager.switch_level(Kwakwa())


def loop():
    global finish, screen, console

    add_button('quit', ['LCTRL+q'])
    add_button('reset', ['r'])

    if CONST.render != 'kivy':
        init_level()

    if CONST.render == 'pookoo':
        log(dir(pookoo))
        pookoo.audio.begin()

    if CONST.render != 'kivy':
        while not finish:
            if CONST.render == 'pookoo':
                pookoo.draw.clear()
            elif CONST.render == 'sfml':
                img_manager.clear_screen(screen)
            update_event()
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
            elif CONST.render == 'pookoo':
                pookoo.audio.step()
                pookoo.window.step()
    else:
        App.get_running_app().run()

    if CONST.render == 'sfml':
        screen.close()
    elif CONST.render == 'pookoo':
        pookoo.audio.finish()
        pookoo.window.finish()

'''
def start():
    global screen
    log("START")

