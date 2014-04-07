'''
Rect type useful for collision with GUI button
or to know the center of a rectangle

Created on Feb 1, 2014

@author: efarhan
'''

from engine.const import  log, CONST
from engine.vector import Vector2

if CONST.render == 'sfml':
    import sfml


class Rect():
    def __init__(self,pos, size,angle=0):
        self.pos = pos
        self.size = size
        if not self.size:
            self.size = Vector2()

        if CONST.render == 'sfml':
            self.rect = sfml.Rectangle(self.pos.get_tuple(),self.size.get_tuple())

    def set_center(self,center_pos):
        self.pos = center_pos-self.size/2

    def get_center(self):
        if CONST.render == 'sfml':
            return self.rect.center
        
        return Vector2(self.pos+self.size/2)

    def collide_point(self,point_pos):
        log("Rect-Point collision: {0} {1} {2}".format(str(self.pos.get_tuple()), str(self.size.get_tuple()), str(point_pos.get_tuple())))
        status = (self.pos.x < point_pos.x < self.pos.x+self.size.x and
                  self.pos.y < point_pos.y < self.pos.y+self.size.y)
        return status