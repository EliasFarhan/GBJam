'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.const import log,CONST
from event.keyboard_event import button_map
if CONST.render == 'sfml':
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


def update_joy_event():
    global joystick

    if CONST.render == 'sfml':
        joystick = sfml.Joystick
        for joy in range(sfml.Joystick.COUNT):
            if sfml.Joystick.is_connected(joy):
                for i in range(sfml.Joystick.AXIS_COUNT):
                    if sfml.Joystick.has_axis(joy,i):
                        if i < 6:
                            axis['JOY'+str(joy)+'AXIS'+str(i)] = sfml.Joystick.get_axis_position(joy, i)
                        else:
                            axis['JOY'+str(joy)+'HAT'+str(i-6)] = sfml.Joystick.get_axis_position(joy, i)
                for i in range(sfml.Joystick.get_button_count(joy)):
                    button_value['JOY'+str(joy)+'BUTTON'+str(i)] = sfml.Joystick.is_button_pressed(joy, i)


def get_joy_button(action):
    global button_map,button_value
    if joystick:
        try:
            button_key_list = button_map[action]
            value = False
            for button_key in button_key_list:
                if 'BUTTON' in button_key:
                    
                    value = value or button_value["".join(button_key.split('_'))]
                elif 'AXIS' in button_key:
                    parameters = button_key.split('_')
                    axis_name = "".join(parameters[0:len(parameters)-1])

                    if parameters[-1] == '-':
                        value = value or axis[axis_name] < -50
                    elif parameters[-1] == '+':
                        value = value or axis[axis_name] > 50
                elif 'HAT' in button_key:
                    pass
            return value
        except KeyError:
            pass

    return False


def add_joy_button(action, button_list):
    global joystick
    button_map[action] = button_list
