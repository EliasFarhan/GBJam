'''
Manage the font loading and rendering

Created on Feb 19, 2014

@author: efarhan
'''
from engine.const import CONST, log
from numbers import Number
from engine.vector import Vector2

if CONST.render == 'sfml':
    import sfml
elif CONST.render == 'pookoo':
    pass
fonts = {}

def pixel2point(pixel):
    return int(pixel*3/4)

def load_font(name,size):
    '''Use pixel size'''
    global fonts
    if CONST.render == 'pookoo' or CONST.render == 'kivy':
        log("Font not yet implemented",1)
        return

    try:
        fonts[name]
    except KeyError:
        try:
            if CONST.render == 'sfml':
                fonts[name] = sfml.Font.from_file(name)
        except IOError:
            if CONST.render == 'sfml':
                return None
    return fonts[name]


def load_text(font,text,color=(0,0,0),size=0):
    if CONST.render == 'sfml':
        if font and size:
            text = sfml.Text(text)
            text.font = font
            if isinstance(size,Number):
                text.character_size = pixel2point(size)
            elif isinstance(size,Vector2):
                text.character_size = pixel2point(size.y)
            text.color = sfml.Color(color[0], color[1], color[2])
            return text
        
    return None