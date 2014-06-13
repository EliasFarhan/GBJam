
'''
Manage physics, input event 
and create a root for Event Engine 

Created on 8 sept. 2013

@author: efarhan
'''
'''

"""
from input.keyboard_input import update_keyboard_event, get_key_button,\
    add_key_button
from engine.const import CONST, log
from input.joystick_input import get_joy_button, add_joy_button,\
    update_joy_event
from engine.level_manager import get_level
from engine.vector import Vector2

if CONST.render == 'sfml':
    import sfml


def add_button(action, key_list):
    add_joy_button(action, key_list)
    add_key_button(action, key_list)


def get_button(action):
    return get_key_button(action) or get_joy_button(action)


def get_current_button():
    #TODO: return all current keys events
    pass


def update_event():
    """
    Update the states of Input Event
    """

    if CONST.render == 'sfml':
        from engine.init import engine
        window = engine.screen
        update_joy_event()
        for event in window.events:
            update_keyboard_event(event)
            
            if type(event) is sfml.CloseEvent:
                from engine.init import engine
                engine.finish = True
            elif type(event) is sfml.MouseButtonEvent:
                screen_ratio = float(engine.get_screen_size().y)/Vector2(engine.screen.size).y
                from levels.gamestate import GameState
                if get_level().__class__ == GameState:
                    log((Vector2(event.position)*screen_ratio+get_level().screen_pos).get_tuple())
            elif type(event) is sfml.ResizeEvent:
                new_size = event.size
    elif CONST.render == 'pookoo':
        update_keyboard_event()


'''