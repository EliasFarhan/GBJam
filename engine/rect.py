'''
Rect type useful for collision with GUI button
or to know the center of a rectangle

Created on Feb 1, 2014

@author: efarhan
'''

from engine.const import pookoo, log

if not pookoo:
    import pygame

class Rect():
    def __init__(self,pos, size):
        self.pos = pos
        self.size = size
        if not pookoo:
            self.rect = pygame.Rect(pos,size)
    def get_center(self):
        if pookoo:
            return (self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2)
        else:
            return self.rect.center
    def collide_point(self,point_pos):
        
        status = False
        '''if pookoo:
            status = (self.pos[0] < point_pos[0] < self.pos[0]+self.size[0] and
                    self.pos[1] < point_pos[1] < self.pos[1]+self.size[1])
        else:
            status = self.rect.collidepoint(point_pos)'''
        status = (self.pos[0] < point_pos[0] < self.pos[0]+self.size[0] and
                    self.pos[1] < point_pos[1] < self.pos[1]+self.size[1])
        log("Status: "+str(status)+" "+str(point_pos)+" "+str(self.pos)+" "+str(self.size))
        return status