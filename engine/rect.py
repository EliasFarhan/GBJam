'''
Rect type useful for collision with GUI button
or to know the center of a rectangle

Created on Feb 1, 2014

@author: efarhan
'''

from engine.const import log,CONST
from engine.vector import Vector2

if CONST.render == 'sfml':
    import sfml
class Rect():
    def __init__(self,pos, size,angle=0):
        self.pos = pos
        self.size = size

        if CONST.render == 'sfml':
            self.rect = sfml.Rectangle(self.pos.get_tuple(),self.size.get_tuple())
    def set_center(self,center_pos):
        self.pos = center_pos-self.size/2
    def get_center(self):
        if CONST.render == 'sfml':
            return self.rect.center
        
        return (self.pos[0]+self.size[0]/2, self.pos[1]+self.size[1]/2)
    def collide_point(self,point_pos):
        status = (self.pos[0] < point_pos[0] < self.pos[0]+self.size[0] and
                    self.pos[1] < point_pos[1] < self.pos[1]+self.size[1])
        log("Status: "+str(status)+" "+str(point_pos)+" "+str(self.pos)+" "+str(self.size))
        return status