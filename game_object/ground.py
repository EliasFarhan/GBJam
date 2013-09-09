'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object import GameObject
import pygame
class Ground(GameObject):
    def __init__(self, screen_size,topleft_pos, nmb_block,physics):
        # set size
        GameObject.__init__(self,physics)
        self.block_size = (32,32)
        self.nmb_block = nmb_block
        self.size = (self.block_size[0]*self.nmb_block[0],self.block_size[1]*self.nmb_block[1])
        self.rect = pygame.Rect(topleft_pos,self.size)
        self.pos = self.rect.center
        self.img = 0
        self.load_images()
        self.init_physics()
    def load_images(self):
        #load block
        self.img = self.img_manager.load_with_size('data/sprites/block/block1.png', self.block_size)
    def loop(self,screen,screen_pos):
        for i in range(self.nmb_block[0]):
            for j in range(self.nmb_block[1]):
                self.img_manager.show(self.img, screen, \
                    (\
                    self.rect.left+self.block_size[0]/2+i*self.block_size[0]-screen_pos[0],\
                    self.rect.top+self.block_size[1]/2+j*self.block_size[1]-screen_pos[1]\
                    )\
                                      )

