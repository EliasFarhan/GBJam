'''
Created on Feb 19, 2014

@author: efarhan
'''
from game_object.game_object_main import GameObject
from engine.font_manager import load_font, load_text
from engine.rect import Rect
from engine.const import log
from engine.image_manager import show_image

class Text(GameObject):
    def __init__(self,pos,size,font,text,angle=0,color=(0,0,0),gradient=0,center=False):
        GameObject.__init__(self)
        self.pos = pos
        self.center = center
        self.size = size
        self.color = color
        self.font = load_font(font,size)
        self.set_text(text)
        self.gradient = gradient
        self.time = 1
        self.relative = False
    def set_text(self,text):
        self.text = text
        self.time = 1
        self.change_text(text)
    def change_text(self,text,color=None):
        
        new_color = color
        if color == None:
            new_color = self.color
        self.text_surface = load_text(self.font,text,new_color)
        if self.text_surface:
            self.size = self.text_surface.get_size()
            self.update_rect()
        
    def loop(self,screen,screen_pos):
        if self.time < self.gradient:
            self.time += 1
            self.change_text(self.text[0:int(self.time/self.gradient*len(self.text))])
        pos = self.pos
        if self.relative:
            pass
        show_image(self.text_surface, screen, pos, self.angle, self.center, new_size, rot_func, factor, center_image)
        screen.blit(self.text_surface,self.pos)