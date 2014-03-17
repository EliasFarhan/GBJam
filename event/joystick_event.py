'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.const import log, render
if render == 'pygame':
    import pygame
elif render == 'sfml':
    import sfml

from symbol import parameters
joystick = None

'''button_map = {'action' : 'key'}'''
button_map = {}

'''button_value = {'key' : value}'''
button_value = {}

'''axis'''
axis = {}

hat = {}
def joystick_init():
    global joystick
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        if 'XBOX' in joystick.get_name():
            log("An XBOX controller is plug in")
        joystick.init()
def update_joy_event():
    global joystick
    if joystick:
        for i in range(joystick.get_numaxes()):
            axis['AXIS'+str(i)] = joystick.get_axis(i)
        for i in range(joystick.get_numhats()):
            axis['HAT'+str(i)] = joystick.get_axis(i)
        for i in range(joystick.get_numbuttons()):
            button_value['BUTTON'+str(i)] = joystick.get_button(i)
def get_joy_button(action):
    global button_map,button_value
    if joystick:
        try:
            button_key = button_map[action]
            if 'BUTTON' in button_key:
                return button_value[button_map[action]]
            elif 'AXIS' in button_key:
                parameters = button_key.split('_')
                if int(parameters[1]) < joystick.get_numaxes():
                    if parameters[2] == "-":
                        return (axis[parameters[0]+parameters[1]]<-0.9)
                    else:
                        return (axis[parameters[0]+parameters[1]]>0.9)
        except KeyError:
            pass
    return False
def add_joy_button(action, button):
    global joystick
    if joystick:
        parameters = button.split('_')
        if parameters[0] == 'JOY':
            if parameters[1] == 'BUTTON':
                button_map[action] = 'BUTTON'+parameters[2]
            elif parameters[1] == 'AXIS':
                button_map[action] = "_".join(parameters[1:len(parameters)])
        