'''
Manage physics, input event 
and create a root for Event Engine 

Created on 8 sept. 2013

@author: efarhan
'''

from engine.const import pookoo, log
from engine.init import resize_screen
if not pookoo:
    import pygame
else:
    import input
    

class Event():
    def __init__(self):
        self.parent_event = None # for dialog only
        self.next_event = None
    def set_parent_event(self,parent_event):
        self.parent_event = parent_event
        if self.next_event == None:
            self.next_event = parent_event.next_event
    def execute(self):
        if self.next_event:
            self.next_event.execute()
        #for dialog tree only
        elif self.parent_event:
            if self.parent_event.next_event:
                self.parent_event.next_event.execute()


class KEY():
    if not pookoo:
        K_UP = pygame.K_UP
        K_DOWN = pygame.K_DOWN
        K_LEFT = pygame.K_LEFT
        K_RIGHT = pygame.K_RIGHT
        K_ESCAPE = pygame.K_ESCAPE
    else:
        K_UP = 82
        K_DOWN = 81
        K_LEFT = 80
        K_RIGHT = 79
        K_ESCAPE = 41


physics_events = []

def add_physics_event(event):
    global physics_events
    physics_events.append(event)
def get_physics_event():
    global physics_events
    result = []
    for i in range(len(physics_events)):
        result.append(physics_events.pop())
    return result


class PhysicsEvent:
    def __init__(self,a,b,begin):
        self.a=a
        self.b=b
        self.begin=begin

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
    
def update_event():
    global button_key,button_value
    if not pookoo:
        for event in pygame.event.get():
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
            elif event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)
    else:
        for k_value in button_key.keys():
            button_value[button_key[k_value]] = input.keyboard_pressed(k_value)

def get_mouse():
    return pygame.mouse.get_pos(), pygame.mouse.get_pressed()

def show_mouse(show=True):
    if not pookoo:
        pygame.mouse.set_visible(show)


    
