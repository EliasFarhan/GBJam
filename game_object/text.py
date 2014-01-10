'''
Created on 24 sept. 2013

@author: efarhan
'''
import pygame
from game_object.game_object import GameObject

class Text(GameObject):
    def __init__(self,pos,text,size=72,alpha=255, alpha_increase=False, alpha_decrease=False):
        #GameObject.__init__(self, physics=None, img_path='', size, pos)
        self.pos = pos
        self.text = text
        self.font = pygame.font.Font('data/font/8-BITWONDER.ttf',size)
        self.alpha = alpha
        self.msg_surface_obj = self.font.render(self.text, False, pygame.Color(255, 255, 255))
        self.increase_alpha = alpha_increase
        self.decrease_alpha = alpha_decrease
    def loop(self, screen,screen_pos):
        self.msg_surface_obj.set_alpha(self.alpha)
        if(self.increase_alpha and self.alpha < 255):
            self.alpha += 2
            if self.alpha > 255:
                self.alpha = 255
        elif(self.alpha == 255):
            self.increase_alpha = False
        
        if(self.decrease_alpha and self.alpha > 0):
            self.alpha -= 2
            if(self.alpha<0):
                self.alpha = 0
        elif(self.alpha == 0):
            self.decrease_alpha = False
        msg_rect_obj = self.msg_surface_obj.get_rect()
        msg_rect_obj.midtop = (self.pos[0]-screen_pos[0], self.pos[1]-screen_pos[1])
        screen.blit(self.msg_surface_obj, msg_rect_obj)
    def set_text(self, text):
        self.text = text
        self.msg_surface_obj = self.font.render(self.text, False, pygame.Color(0, 0, 0))