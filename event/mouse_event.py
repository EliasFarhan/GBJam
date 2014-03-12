'''
Created on Feb 26, 2014

@author: efarhan
'''
from engine.const import render

if render == 'pygame':
    import pygame

def get_mouse():
    '''
    Return mouse state as 
    position, (left, middle, right)
    '''
    return pygame.mouse.get_pos(), pygame.mouse.get_pressed()

def show_mouse(show=True):
    '''
    Show mouse on display
    '''
    if render == 'pygame':
        pygame.mouse.set_visible(show)