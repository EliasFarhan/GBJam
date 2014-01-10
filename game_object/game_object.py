'''
Created on 25 aout 2013

@author: efarhan
'''
import pygame

from engine.image_manager import show_image,load_image_with_size

class GameObject():
    def __init__(self,physics, img_path='', size=None,pos=None):
        if(pos == None):
            self.pos = (0, 0)
        else:
            self.pos = pos
        self.size = (0, 0)
        self.physics = physics
        if(size != None):
            self.load_image(img_path, size)
    def loop(self,screen,screen_pos):
        show_image(self.img, screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]))
    def init_physics(self):
        self.physics.add_static_object(self)
    def load_image(self,img_path,size):
        self.img = load_image_with_size(img_path, size)



        

