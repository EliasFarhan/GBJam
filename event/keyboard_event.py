'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.const import CONST, log


if CONST.render == 'sfml':
    import sfml


class KEY():
    if CONST.render == 'sfml':
        K_UP = sfml.Keyboard.UP
        K_DOWN = sfml.Keyboard.DOWN
        K_LEFT = sfml.Keyboard.LEFT
        K_RIGHT = sfml.Keyboard.RIGHT
        K_ESCAPE = sfml.Keyboard.ESCAPE
        K_LCTRL = sfml.Keyboard.L_CONTROL
        K_RCTRL = sfml.Keyboard.R_CONTROL
        K_ENTER = sfml.Keyboard.RETURN
        K_A = sfml.Keyboard.A
        K_Z = sfml.Keyboard.Z
    elif CONST.render == 'pookoo':
        pass

'''button_map = {'action' : 'key_list'}'''
button_map = {}

'''button_value = {'key' : value}'''
button_value = {}

'''button_key = {'render_key': 'key'}'''
button_key = {}


def add_one_key(key_value):
    if CONST.render == 'pookoo':
        log("Error: KEYS not yet implemented",1)
        return
    button_value[key_value] = 0
    try:
        if ord('a') <= ord(key_value) <= ord('z'):
            button_key[ord(key_value)-ord('a')+KEY.K_A] = key_value
    except TypeError:
        '''the key value is not a letter or a number'''
        if key_value == 'UP':
            button_key[KEY.K_UP] = key_value
        if key_value == 'DOWN':
            button_key[KEY.K_DOWN] = key_value
        if key_value == 'LEFT':
            button_key[KEY.K_LEFT] = key_value
        if key_value == 'RIGHT':
            button_key[KEY.K_RIGHT] = key_value
        if key_value == 'ESC':
            button_key[KEY.K_ESCAPE] = key_value
        if key_value == 'RCTRL':
            button_key[KEY.K_RCTRL] = key_value
        if key_value == 'LCTRL':
            button_key[KEY.K_LCTRL] = key_value
        if key_value == 'ENTER':
            button_key[KEY.K_ENTER] = key_value


def add_key_button(action,key_list):
    global button_map,button_value,button_key
    button_map[action] = key_list
    for key_value in key_list:
        keys = key_value.split("+")
        for k in keys:
            add_one_key(k)


def get_current_key():
    current_keys = []
    for key in button_value.keys():
        if button_value[key]:
            current_keys.append(key)
    return current_keys

            
def get_key_button(action):
    global button_value, button_map
    try:
        value = False
        for key in button_map[action]:
            if "+" in key:
                key_value = True
                for k in key.split("+"):
                    key_value = key_value and button_value[k]
                value = (value or key_value)
            else:
                value = (value or button_value[key])
        return value
    except KeyError:
        return False


def update_keyboard_event(event):
    global button_value,button_key
    '''
    Update the states of Input Event
    '''
    if CONST.render == 'sfml':
        if type(event) == sfml.KeyEvent:
            try:
                button_value[button_key[event.code]] = event.pressed
            except KeyError:
                '''Key not in map'''
                pass
