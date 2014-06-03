'''
Created on Feb 19, 2014

@author: efarhan
'''
from game_object.game_object_main import GameObject
from engine.font_manager import load_font, load_text
from engine.const import log, CONST
from engine.img_manager import show_image
from engine.vector import Vector2

class Text(GameObject):
    def __init__(self,pos,size,font,text,angle=0,color=(0,0,0),gradient=0,center=False,relative=False):
        GameObject.__init__(self)
        self.pos = pos
        self.center = center
        self.character_size = size
        self.color = color
        self.font = load_font(font,self.character_size)
        self.set_text(text)
        self.gradient = gradient
        self.time = 1
        self.screen_relative = relative

    def set_text(self,text):
        self.text = text
        self.time = 1
        self.change_text(text)

    def change_text(self,text,color=None):
        
        new_color = color
        if color == None:
            new_color = self.color
        if text != '':
            self.text_surface = load_text(self.font,text,new_color,self.character_size)
        else:
            self.text_surface = None
            return
        if self.text_surface:
            if CONST.render == 'sfml':
                sfml_size = (self.text_surface.global_bounds.width,self.text_surface.global_bounds.height)
                self.size = Vector2(sfml_size)
            if self.size:
                self.update_rect()
        if self.text_surface:
            self.text_surface.position = self.pos.get_tuple()

    def loop(self,screen,screen_pos):
        if self.text_surface:
            if self.time < self.gradient:
                self.time += 1
                self.change_text(self.text[0:int(self.time/self.gradient*len(self.text))])
            pos = self.pos
            if not self.screen_relative:
                pos = pos-screen_pos
            if self.center and self.size:
                pos = pos - Vector2(self.size.x/2.0, 0.0)
            show_image(self.text_surface, screen, pos, self.angle, self.center, new_size=self.size)
        #screen.blit(self.text_surface,self.pos)

    @staticmethod
    def parse_image(image_data, pos, size, angle):
        return None
