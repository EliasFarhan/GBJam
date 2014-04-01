"""
Created on Feb 26, 2014

@author: efarhan
"""
from engine.const import CONST
from engine.vector import Vector2


if CONST.render == 'sfml':
    import sfml


def get_mouse():
    """
    Return mouse state as
    position, (left, right,middle)
    """
    if CONST.render == 'sfml':
        return Vector2(sfml.Mouse.get_position()), [sfml.Mouse.is_button_pressed(sfml.Mouse.LEFT),
                                           sfml.Mouse.is_button_pressed(sfml.Mouse.RIGHT),
                                           sfml.Mouse.is_button_pressed(sfml.Mouse.MIDDLE)]


def show_mouse(show=True):
    """Show/hide mouse"""

    if CONST.render == 'sfml':
        from engine.loop import get_screen
        get_screen().mouse_cursor_visible = show