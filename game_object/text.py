'''
Created on Feb 19, 2014

@author: efarhan
'''
from game_object.game_object import GameObject
from engine.font_manager import load_font, load_text
from engine.rect import Rect
from engine.const import log

class Text(GameObject):
    def __init__(self,pos,size,font,text,color=(0,0,0),gradient=0):
        GameObject.__init__(self)
        self.pos = pos
        self.color = color
        self.font = load_font(font,size)
        self.set_text(text)
        self.gradient = gradient
        self.time = 1
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
            self.rect = Rect(self.pos, self.size)
        
    def loop(self,screen,screen_pos):
        if self.time < self.gradient:
            self.time += 1
            self.change_text(self.text[0:int(self.time/self.gradient*len(self.text))])
        screen.blit(self.text_surface,self.pos)