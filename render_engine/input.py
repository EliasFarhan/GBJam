from engine.const import CONST


__author__ = 'efarhan'


class Input():
    def __init__(self):
        pass

    def init(self):
        self.init_keyboard()
        self.init_joystick()

    def add_button(self,action,key_list):
        pass

    def get_button(self,action):
        pass

    def get_current_button(self):
        pass

    def init_keyboard(self):
        """button_map = {'action' : 'key_list'}"""
        self.button_map = {}

        '''button_value = {'key' : value}'''
        self.button_value = {}

        '''button_key = {'render_key': 'key'}'''
        self.button_key = {}

    def init_joystick(self):

        '''axis'''
        self.axis = {}

        self.hat = {}


input_manager = Input()

if CONST.render == 'sfml':
    from render_engine.sfml_engine.sfml_input import SFMLInput
    input_manager = SFMLInput()
