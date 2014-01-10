'''
Created on 8 sept. 2013

@author: efarhan
'''
import pygame


from game_object.game_object import GameObject
from animation.platformer_animation import PlatformerAnimation

from physics.physics import pixel2meter



class Player(GameObject):
    def __init__(self,physics,move=0,jump=1,factor=1):
        GameObject.__init__(self,physics)
        self.size = (64,64)
        self.box_size = (18,21)
        
        if(factor != 1):
            self.size = (factor*self.size[0],factor*self.size[1])
            self.box_size = (factor*self.box_size[0],factor*self.box_size[1])
            self.foot_sensor_size = (factor*self.foot_sensor_size[0],factor*self.foot_sensor_size[1])
        self.anim = PlatformerAnimation(self.img_manager,self.size)
        self.anim.jump = jump
        self.anim.load_images()
        self.anim.physics = physics
        self.anim.init_physics(self)
        self.anim.move = move
        self.invulnerability = 0

        self.font = pygame.font.Font('data/font/8-BITWONDER.ttf',25)
    def set_animation(self,anim):
        physics = self.anim.physics
        self.anim = anim
        self.anim.physics = physics
        self.anim.load_images()

    def loop(self, screen,screen_pos,new_size=1):

        self.anim.loop(self)
        
        # show the current img
        self.pos = (int(self.pos[0]), int(self.pos[1]))
        new_screen_pos = self.pos
        if(self.anim.invulnerability%2!= 1):
            self.img_manager.show(self.anim.img, screen, (self.pos[0]-new_screen_pos[0],self.pos[1]-new_screen_pos[1]),factor=new_size)
        return self.pos
    
    def set_position(self,new_pos):
        self.pos = new_pos
        self.anim.body.position = (pixel2meter(new_pos[0]),pixel2meter(new_pos[1]))
        