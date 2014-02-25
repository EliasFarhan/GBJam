'''
Manage the font loading and rendering

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
            if not pookoo:
                fonts[name] = pygame.font.Font(name, pixel2point(size))
            else:
                try:
                    fonts[name] = font.open(name)
                except ValueError:
                    return None
        except IOError:
            fonts[name] = pygame.font.SysFont(name, pixel2point(size))
    return fonts[name]
def load_text(font,text,color=(0,0,0)):
    if font:
        return font.render(text,False,color)
    return None