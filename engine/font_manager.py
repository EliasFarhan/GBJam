'''
Manage the font loading and rendering

Created on Feb 19, 2014

@author: efarhan
'''
from engine.const import render, log


if render == 'pygame':
    import pygame
elif render == 'sfml':
    import sfml
    
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
            elif render == 'sfml':
                fonts[name] = sfml.Font.from_file(name)
        except IOError:
            if render == 'pygame':
                fonts[name] = pygame.font.SysFont(name, pixel2point(size))
            elif render == 'sfml':
                return None
    return fonts[name]
def load_text(font,text,color=(0,0,0),size=0):
    if render == 'pygame':
        if font:
            return font.render(text,False,color)
    elif render == 'sfml':
        if font and size:
            text = sfml.Text(text)
            text.font = font
            text.character_size = pixel2point(size)
            text.color = sfml.Color(color[0],color[1],color[2])
            return text
        
    return None