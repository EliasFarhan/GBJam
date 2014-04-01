
'''
Manage physics, input event 
and create a root for Event Engine 

Created on 8 sept. 2013

@author: efarhan
'''


from event.keyboard_event import update_keyboard_event, get_key_button,\
    add_key_button
from engine.const import CONST, log
from event.joystick_event import get_joy_button, add_joy_button,\
    update_joy_event
from engine.level_manager import get_level
from engine.vector import Vector2

if CONST.render == 'pygame':
    import pygame
elif CONST.render == 'sfml':
    import sfml


def add_button(action, key_list):
    add_joy_button(action, key_list)
    add_key_button(action, key_list)


def get_button(action):
    return get_key_button(action) or get_joy_button(action)


def update_event():
    '''
    Update the states of Input Event
    '''

    if CONST.render == 'sfml':
        from engine.loop import get_screen
        window = get_screen()
        update_joy_event()
        for event in window.events:
            update_keyboard_event(event)
            
            if type(event) is sfml.CloseEvent:
                from engine.loop import set_finish
                set_finish()
            elif type(event) is sfml.MouseButtonEvent:
                from engine.init import get_screen_size
                screen_ratio = float(get_screen_size().y)/Vector2(get_screen().size).y
                from levels.gamestate import GameState
                if get_level().__class__ == GameState:
                    log((Vector2(event.position)*screen_ratio+get_level().screen_pos).get_tuple())

