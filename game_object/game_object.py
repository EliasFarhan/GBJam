'''
Created on 25 aout 2013

@author: efarhan
'''
import pygame

from engine.image_manager import img_manager

class GameObject():
    def __init__(self,physics):
        self.img_manager = img_manager
        self.pos = (0, 0)
        self.size = (0, 0)
        self.physics = physics
    def loop(self,screen):
        pass
    def init_physics(self):
        self.physics.add_static_object(self)
    



        

