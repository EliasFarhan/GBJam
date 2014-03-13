'''
Manage the font loading and rendering

Created on Feb 19, 2014

@author: efarhan
'''
from engine.const import render


if render == 'pygame':
    import pygame
    
fonts = {}

def pixel2point(pixel):
    return int(pixel*3/4)

def load_font(name,size):
    '''Use pixel size'''
    global fonts
    try:
        fonts[name]
    except KeyError:
        try:
            if render == 'pygame':
                fonts[name] = pygame.font.Font(name, pixel2point(size))
        except IOError:
            fonts[name] = pygame.font.SysFont(name, pixel2point(size))
    return fonts[name]
def load_text(font,text,color=(0,0,0)):
    if font:
        return font.render(text,False,color)
    return None