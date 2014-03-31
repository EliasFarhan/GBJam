'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.const import CONST


if CONST.render == 'sfml':
    import sfml
def get_mouse():
    '''
    Return mouse state as 
    position, (left, middle, right)
    '''
    if CONST.render == 'sfml':
        return sfml.Mouse.get_position(), [sfml.Mouse.is_button_pressed(i) for i in range(3)]
def show_mouse(show=True):
    """Show/hide mouse"""

    if CONST.render == 'sfml':
        from engine.loop import get_screen
        get_screen().mouse_cursor_visible = show