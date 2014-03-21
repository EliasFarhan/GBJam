'''
Rect type useful for collision with GUI button
or to know the center of a rectangle

Created on Feb 1, 2014

@author: efarhan
'''

from engine.const import  log, render

if render == 'pygame':
    import pygame
elif render == 'sfml':
    import sfml
class Rect():
    def __init__(self,pos, size,angle=0):
        self.pos = pos
        self.size = size

        if render == 'pygame':
            self.rect = pygame.Rect(pos,size)
        elif render == 'sfml':
            self.rect = sfml.Rectangle(self.pos.get_tuple(),self.size.get_tuple())
    def set_center(self,center_pos):
        self.pos = (center_pos[0]-self.size[0]/2, center_pos[1]-self.size[1]/2)
    def get_center(self):
        if render == 'sfml':
            return self.rect.center
        
        return (self.pos[0]+self.size[0]/2, self.pos[1]+self.size[1]/2)
    def collide_point(self,point_pos):
        status = (self.pos[0] < point_pos[0] < self.pos[0]+self.size[0] and
                    self.pos[1] < point_pos[1] < self.pos[1]+self.size[1])
        log("Status: "+str(status)+" "+str(point_pos)+" "+str(self.pos)+" "+str(self.size))
        return status