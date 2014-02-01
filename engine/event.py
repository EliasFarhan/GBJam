'''
Created on 8 sept. 2013

@author: efarhan
'''

import pygame
from pygame.locals import *
from engine.const import log
from engine.init import toogle_fullscreen

UP,DOWN,LEFT,RIGHT,ACTION,END,RETRY = 0,0,0,0,0,0,0
UP2,DOWN2,LEFT2,RIGHT2 = 0,0,0,0
joystick = 0
index = 0
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

def init():
    global joystick
    if pygame.joystick.get_count() != 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
def update_event():
    global joystick,index,UP,DOWN,LEFT,RIGHT,ACTION,END,RETRY,UP2,DOWN2,RIGHT2,LEFT2
    # check events (with joystick)
    for event in pygame.event.get(): 
        if (joystick != 0):
            if (event.type == JOYHATMOTION):
                if (joystick.get_hat(0) == (0, 1)):
                    UP = 1
                elif(joystick.get_hat(0) == (0, -1)):
                    # DOWN
                    pass
                elif(joystick.get_hat(0) == (1, 0)):
                    RIGHT = 1
                elif(joystick.get_hat(0) == (-1, 0)):
                    # LEFT
                    LEFT = 1
                elif(joystick.get_hat(0) == (0, 0)):
                    UP, RIGHT,LEFT = 0, 0,0
            elif event.type == JOYAXISMOTION:
                if(joystick.get_axis(0)>0.9):
                    RIGHT = 1
                else:
                    RIGHT = 0
                if(joystick.get_axis(0)<-0.9):
                    LEFT = 1
                else:
                    LEFT = 0
            elif event.type == JOYBUTTONDOWN:
                if(joystick.get_button(1)):
                    UP = 1
                if(joystick.get_button(4)):
                    index -= 1
                if(joystick.get_button(5)):
                    index += 1
            elif event.type == JOYBUTTONUP:
                if(not joystick.get_button(1)):
                    UP = 0
        if event.type == KEYDOWN:
            if event.key == K_UP:
                UP2 = 1
            elif event.key == K_w:
                UP = 1
            elif event.key == K_DOWN:
                DOWN2 = 1
            
            elif event.key == K_s:
                    # DOWN
                DOWN = 1
            elif event.key == K_RIGHT:
                RIGHT2 = 1
                
            elif event.key == K_d:
                RIGHT = 1
            elif event.key == K_LEFT:
                LEFT2 = 1
            elif event.key == K_a:
                    # LEFT
                LEFT = 1
            elif event.key == K_ESCAPE:
                END = 1
            elif event.key == K_r:
                RETRY = 1
            elif event.key == K_f:
                toogle_fullscreen()
            elif event.key == K_TAB:
                if pygame.key.get_mods() & KMOD_CTRL:
                    from engine.loop import get_console
                    console = get_console()
                    console.set_active()
                    console.preserve_events = False
        if event.type == KEYUP:
            if event.key == K_UP:
                UP2 = 0
            elif event.key == K_w:
                UP = 0
            elif event.key == K_DOWN :
                DOWN2 = 0
            elif event.key == K_s:
                    # DOWN
                DOWN = 0
            elif event.key == K_RIGHT :
                RIGHT2 = 0
            elif event.key == K_d:
                RIGHT = 0
            elif event.key == K_LEFT :
                LEFT2 = 0
            elif event.key == K_a:
                    # LEFT
                LEFT = 0
            elif event.key == K_ESCAPE:
                END = 0  
            elif event.key == K_r:
                RETRY = 0        
        if event.type == QUIT:
                END = 1
                
def get_editor_event():
    pass
def get_index():
    global index
    return index
def is_end():
    global END
    return END
def get_keys():
    global RIGHT,LEFT,UP,DOWN,ACTION
    return (RIGHT,LEFT,UP,DOWN,ACTION)
def get_retry():
    global RETRY
    return RETRY
def get_editor_keys():
    return None
def get_mouse():
    return pygame.mouse.get_pos(), pygame.mouse.get_pressed()
    
