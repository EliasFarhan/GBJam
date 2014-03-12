'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.const import render


if render == 'pygame':
    import pygame
elif render == 'sfml':
    import sfml
class KEY():
    if render == 'pygame':
        K_UP = pygame.K_UP
        K_DOWN = pygame.K_DOWN
        K_LEFT = pygame.K_LEFT
        K_RIGHT = pygame.K_RIGHT
        K_ESCAPE = pygame.K_ESCAPE
    elif render == 'sfml':
        K_UP = sfml.Keyboard.UP
        K_DOWN = sfml.Keyboard.DOWN
        K_LEFT = sfml.Keyboard.LEFT
        K_RIGHT = sfml.Keyboard.RIGHT
        K_ESCAPE = sfml.Keyboard.ESCAPE

'''button_map = {'action' : 'key'}'''
button_map = {}

'''button_value = {'key' : value}'''
button_value = {}

'''button_key = {'pygame_key': 'key'}'''
button_key = {}

def add_button(action,key_value):
    global button_map,button_value,button_key
    
    button_map[action] = key_value
    button_value[action] = 0
    
    try:
        if (ord('a') <= ord(key_value) <= ord('z')) or \
        (ord('0') <= ord(key_value) <= ord('9')):
            button_key[ord(key_value)] = key_value
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
            
            
def get_button(action):
    global button_value,button_map
    try:
        return button_value[button_map[action]]
    except KeyError:
        return False
    
def update_keyboard_event(event):
    '''
    Update the states of Input Event
    '''
    if render == 'pygame':
        if event.type == pygame.KEYDOWN:
            try:
                button_value[button_key[event.key]] = True
            except KeyError:
                '''Key not mapped'''
                pass
            if event.key == pygame.K_TAB:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    from engine.loop import get_console
                    console = get_console()
                    console.set_active()
                    console.preserve_events = False
        elif event.type == pygame.KEYUP:
            try:
                button_value[button_key[event.key]] = False
            except KeyError:    
                '''Key not mapped'''
                pass

