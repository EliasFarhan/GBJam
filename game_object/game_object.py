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
    def rotate(self,angle):
        self.angle += angle
    def scale(self,x,y):
        self.size = (self.size[0]+x,self.size[1]+y)
        self.rect = Rect(self.pos, self.size)
    
    def check_click(self,mouse_pos,screen_pos):
        point_pos = (screen_pos[0]+mouse_pos[0], screen_pos[1]+mouse_pos[1])
        return self.rect.collide_point(point_pos)
    
    def move(self,right,down):
        self.pos = (self.pos+right,self.pos+down)