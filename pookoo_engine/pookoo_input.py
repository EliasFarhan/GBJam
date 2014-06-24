import pookoo
from engine.input import Input
from engine.vector import Vector2

__author__ = 'Elias'

KEY_BIND = {
    "UP": 82,
    "DOWN": 81,
    "LEFT": 80,
    "RIGHT": 79,
    "ESCAPE": 41,
    "LCTRL": 224,
    "RCTRL": 228,
    "ENTER": 40,
    "A": 4,
    "Z": 29,
}

class PookooInput(Input):

    def add_button(self,action,key_list):
        pass

    def get_button(self,action):
        pass

    def get_current_button(self):
        pass

    """KEYBOARD"""

    def update_keyboard_event(self,event=None):
        '''
        Update the states of Input Event
        '''
        for render_key in self.button_key.keys():
            self.button_value[self.button_key[render_key]] = pookoo.input.keyboard.pressed(render_key)

    def get_current_key(self):
        current_keys = []
        for key in self.button_value.keys():
            if self.button_value[key]:
                current_keys.append(key)
        return current_keys

    def get_key_button(self, action):
        try:
            value = False
            for key in self.button_map[action]:
                if "+" in key:
                    key_value = True
                    for k in key.split("+"):
                        key_value = key_value and self.button_value[k]
                    value = (value or key_value)
                else:
                    value = (value or self.button_value[key])
            return value
        except KeyError:
            return False

    def add_one_key(self, key_value):
        """
        Add only one key
        """
        self.button_value[key_value] = 0
        try:
            if ord('a') <= ord(key_value) <= ord('z'):
                self.button_key[ord(key_value) - ord('a') + KEY_BIND['A']] = key_value
        except TypeError:
            '''the key value is not a letter or a number'''
            try:
                self.button_key[KEY_BIND[key_value]] = key_value
            except IndexError:
                pass
            except KeyError:
                pass

    def add_key_button(self,action,key_list):
        self.button_map[action] = key_list
        for key_value in key_list:
            keys = key_value.split("+")
            for k in keys:
                self.add_one_key(k)
    """MOUSE"""

    def get_mouse(self):
        """
        Return mouse state as
        position, (left, right,middle)
        """
        from engine.init import engine

        mouse_pos = Vector2(pookoo.input.mouse.position())
        return mouse_pos,\
               [False,False,False]



    def show_mouse(show=True):
        """
        Show/hide mouse
        """
        from engine.init import engine
        engine.screen.mouse_cursor_visible = show

    """JOYSTICK"""


    def update_joy_event(self):
        for joy in range(sfml.Joystick.COUNT):
            if sfml.Joystick.is_connected(joy):
                for i in range(sfml.Joystick.AXIS_COUNT):
                    if sfml.Joystick.has_axis(joy,i):
                        if i < 6:
                            self.axis['JOY'+str(joy)+'AXIS'+str(i)] = sfml.Joystick.get_axis_position(joy, i)
                        else:
                            self.axis['JOY'+str(joy)+'HAT'+str(i-6)] = sfml.Joystick.get_axis_position(joy, i)
                for i in range(sfml.Joystick.get_button_count(joy)):
                    self.button_value['JOY'+str(joy)+'BUTTON'+str(i)] = sfml.Joystick.is_button_pressed(joy, i)

    def get_joy_button(self,action):

        try:
            button_key_list = self.button_map[action]
            value = False
            for button_key in button_key_list:
                if 'BUTTON' in button_key:

                    value = value or self.button_value["".join(button_key.split('_'))]
                elif 'AXIS' in button_key:
                    parameters = button_key.split('_')
                    axis_name = "".join(parameters[0:len(parameters)-1])

                    if parameters[-1] == '-':
                        value = value or self.axis[axis_name] < -50
                    elif parameters[-1] == '+':
                        value = value or self.axis[axis_name] > 50
                elif 'HAT' in button_key:
                    pass
            return value
        except KeyError:
            pass

        return False

    def add_joy_button(self,action, button_list):
        self.button_map[action] = button_list