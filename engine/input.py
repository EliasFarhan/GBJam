from engine.const import CONST


__author__ = 'efarhan'


class Input():
    def __init__(self):
        pass

    def init(self):
        pass


input_manager = Input()

if CONST.render == 'sfml':
    from sfml_engine.sfml_input import SFMLInput
    input_manager = SFMLInput()
