'''
Created on Feb 3, 2014

@author: efarhan
'''
from engine.rect import Rect

class GameObject:
    def __init__(self):
        self.angle = 0
        self.pos = None
        self.size = None
        self.rect = None
    def scale(self,enlargement,speed=1.1):
        scale_speed = speed
        if not enlargement:
            scale_speed = 1/speed
        self.size = (int(self.size[0]*scale_speed),int(self.size[1]*scale_speed))
        self.rect = Rect(self.pos, self.size)
    
    def move(self,horizontal=0,vertical=0):
        self.pos = (self.pos[0]+horizontal,self.pos[1]+vertical)
        self.rect = Rect(self.pos, self.size)
    def rotate(self,right):
        self.angle += right
    
    def check_click(self,mouse_pos,screen_pos):
        point_pos = (screen_pos[0]+mouse_pos[0], screen_pos[1]+mouse_pos[1])
        return self.rect.collide_point(point_pos)
    
