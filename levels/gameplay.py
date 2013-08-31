'''
Created on 25 aout 2013

@author: efarhan
'''
import engine
from engine.scene import Scene
from engine.game_object import GameObject
from engine.game_object import Player
from physics.physics import Physics
import pygame

class Ground(GameObject):
    def __init__(self, topleft_pos, nmb_block):
        # set size
        GameObject.__init__(self)
        self.block_size = (32,32)
        self.nmb_block = nmb_block
        self.size = (self.block_size[0]*self.nmb_block,self.block_size[1])
        self.rect = pygame.Rect(topleft_pos,self.size)
        self.pos = self.rect.center
        print self.rect.left
        self.img = 'data/sprites/block/block1.png'
        self.load_images()
    def load_images(self):
        #load block
        self.img_manager.load_with_size(self.img, self.block_size)
    def loop(self,screen):
        screen_pos = screen.get_rect()
        for i in range(self.nmb_block):
            self.img_manager.show(self.img, screen, (self.rect.midleft[0]+self.block_size[0]/2+i*self.block_size[0]-engine.level_manager.level.screen_pos[0],self.pos[1]-engine.level_manager.level.screen_pos[1]))
        
class GamePlay(Scene):
    def init(self):
        self.screen_pos = (0,0)
        self.physics = Physics()
        self.player = Player()
        self.ground = Ground((-100,-50),10)
        self.physics.init([self.ground], [self.player])
    def loop(self, screen):
        screen.fill(pygame.Color(255, 255, 255))
        self.player.loop(screen)
        self.ground.loop(screen)
        self.physics.loop()