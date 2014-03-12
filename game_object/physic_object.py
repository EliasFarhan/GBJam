'''
Created on 15 dec. 2013

@author: efarhan
'''

import math
from engine.image_manager import draw_rect
from engine.physics import add_static_box, remove_body
from engine.const import debug,log
from engine.rect import Rect
from game_object.game_object_main import GameObject

class Circle():
    pass

class AngleSquare(GameObject):
    def __init__(self,pos,size,angle=0,data=0,sensor=False):
        GameObject.__init__(self)
        self.data = data
        self.pos = pos
        self.size = size
        self.rect = Rect(self.pos,self.size)
        self.angle = angle
        self.index = 0
        
        self.sensor = sensor
        self.init_physics()
        if debug:
            self.click = False

    def init_physics(self):
        self.rad_angle = math.radians(self.angle)
        center_pos = self.rect.get_center()
        self.index = add_static_box(center_pos,
                        (self.size[0]/2,self.size[1]/2),
                        angle=-self.rad_angle,
                        data=self.data,
                        sensor=self.sensor)
    def update_rect(self):
        GameObject.update_rect(self)
        remove_body(self.index)
        self.init_physics()
    def loop(self,screen,screen_pos):
        if debug:
            draw_rect(screen, screen_pos, self.rect, (255,0,0,255), self.angle)
    


