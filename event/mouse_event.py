'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.const import render

if render == 'pygame':
    import pygame
elif render == 'sfml':
    import sfml
def get_mouse():
    '''
    Return mouse state as 
    position, (left, middle, right)
    '''
    if render == 'pygame':
        return pygame.mouse.get_pos(), pygame.mouse.get_pressed()
    elif render == 'sfml':
        return sfml.Mouse.get_position(), [sfml.Mouse.is_button_pressed(i) for i in range(3)]
def show_mouse(show=True):
    '''
    Show mouse on display
    '''
    if render == 'pygame':
        pygame.mouse.set_visible(show)