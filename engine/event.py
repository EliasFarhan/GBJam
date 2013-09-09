'''
Created on 8 sept. 2013

@author: efarhan
'''

import pygame
from pygame.locals import *

UP,DOWN,LEFT,RIGHT,ACTION,END,RETRY = 0,0,0,0,0,0,0
joystick = 0
def init():
    global joystick
    if pygame.joystick.get_count() != 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
def loop():
    global joystick,UP,DOWN,LEFT,RIGHT,ACTION,END,RETRY
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
            elif event.type == JOYBUTTONUP:
                if(not joystick.get_button(1)):
                    UP = 0
        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == K_w:
                UP = 1
            elif event.key == K_DOWN or event.key == K_s:
                    # DOWN
                DOWN = 1
            elif event.key == K_RIGHT or event.key == K_d:
                RIGHT = 1
            elif event.key == K_LEFT or event.key == K_a:
                    # LEFT
                LEFT = 1
            elif event.key == K_ESCAPE:
                END = 1
            elif event.key == K_r:
                RETRY = 1
        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_w:
                UP = 0
            elif event.key == K_DOWN or event.key == K_s:
                    # DOWN
                DOWN = 0
            elif event.key == K_RIGHT or event.key == K_d:
                RIGHT = 0
            elif event.key == K_LEFT or event.key == K_a:
                    # LEFT
                LEFT = 0
            elif event.key == K_ESCAPE:
                END = 0  
            elif event.key == K_r:
                RETRY = 0        
        if event.type == QUIT:
                END = 1
def end():
    global END
    return END
def get_keys():
    global RIGHT,LEFT,UP,DOWN,ACTION
    return (RIGHT,LEFT,UP,DOWN,ACTION)
def get_retry():
    global RETRY
    return RETRY