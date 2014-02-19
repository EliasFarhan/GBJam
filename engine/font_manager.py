'''
Created on Feb 19, 2014

@author: efarhan
'''
from engine.const import pookoo

if pookoo:
    import font
else:
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
            fonts[name] = pygame.font.Font(name, pixel2point(size))
        except IOError:
            fonts[name] = pygame.font.SysFont(name, pixel2point(size))
    return fonts[name]
def load_text(font,text,color=(0,0,0)):
    return font.render(text,False,color)