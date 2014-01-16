'''
Created on 15 dec. 2013

@author: efarhan
'''
import pygame
import math
from engine.image_manager import rot_center
from physics.physics import pixel2meter
from engine.const import debug

class AngleSquare():
    def __init__(self,pos,size,angle=0,data=0,sensor=False):
        self.data = data
        self.pos = pos
        self.size = size
        self.angle = angle
        
        self.init_debug_physics()
        
        self.sensor = sensor
        self.init_physics()
    def init_debug_physics(self):
    	self.rect = pygame.Rect(self.pos, self.size)
    	self.surface = pygame.Surface(self.size,flags=pygame.SRCALPHA)
    	self.surface.fill(pygame.Color(255,0,0,255))
    def init_physics(self):
        self.rad_angle = math.radians(self.angle)
        center_pos = self.rect.center
        self.index = self.physics.add_static_box(center_pos,self.size,angle=-self.rad_angle,data=self.data,sensor=self.sensor)
    def loop(self,screen,screen_pos):
        if debug:
            rot_image, rot_rect = rot_center(self.surface, self.rect, self.angle)
            screen.blit(rot_image, (rot_rect[0]-screen_pos[0],rot_rect[1]-screen_pos[1]))