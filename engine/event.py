'''
Created on 8 sept. 2013

@author: efarhan
'''

import pygame
from pygame.locals import *
from engine.const import pookoo, log

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
            button_key[K_UP] = key_value
        if key_value == 'DOWN':
            button_key[K_DOWN] = key_value
        if key_value == 'LEFT':
            button_key[K_LEFT] = key_value
        if key_value == 'RIGHT':
            button_key[K_RIGHT] = key_value
        if key_value == 'ESC':
            button_key[K_ESCAPE] = key_value
            
            
def get_button(action):
    global button_value,button_map
    try:
        return button_value[button_map[action]]
    except KeyError:
        return False
    
def update_event():
    global button_key,button_value
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            try:
                button_value[button_key[event.key]] = True
            except KeyError:
                '''Key not mapped'''
                pass
        elif event.type == KEYUP:
            try:
                button_value[button_key[event.key]] = False
            except KeyError:
                '''Key not mapped'''
                pass

def get_mouse():
    return pygame.mouse.get_pos(), pygame.mouse.get_pressed()

def show_mouse(show=True):
    if not pookoo:
        pygame.mouse.set_visible(show)
    
