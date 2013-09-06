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
    def __init__(self, topleft_pos, nmb_block,physics):
        # set size
        GameObject.__init__(self,physics)
        self.block_size = (32,32)
        self.nmb_block = nmb_block
        self.size = (self.block_size[0]*self.nmb_block,self.block_size[1])
        self.rect = pygame.Rect(topleft_pos,self.size)
        self.pos = self.rect.center
        self.img = 0
        self.load_images()
        self.init_physics()
    def load_images(self):
        #load block
        self.img = self.img_manager.load_with_size('data/sprites/block/block1.png', self.block_size)
    def loop(self,screen):
        screen_pos = screen.get_rect()
        for i in range(self.nmb_block):
            self.img_manager.show(self.img, screen, \
                    (\
                     self.rect.midleft[0]+self.block_size[0]/2+i*self.block_size[0]-engine.level_manager.level.screen_pos[0],\
                     self.pos[1]-engine.level_manager.level.screen_pos[1])\
                                  )

class Electricity(GameObject):
    def __init__(self, angle=0):
        self.angle = angle
        
class GamePlay(Scene):
    def init(self):
        self.screen_pos = (0,0)
        self.physics = Physics()
        self.physics.init()
        self.player = Player(self.physics)
        self.ground = Ground((-100,-100),120,self.physics)
        self.floor_one = Ground((300, 0), 60,self.physics)
        self.floor_two = Ground((600, 100), 60,self.physics)

    def loop(self, screen):
        screen.fill(pygame.Color(255, 255, 255))
        self.physics.loop()
        self.ground.loop(screen)
        self.floor_one.loop(screen)
        self.floor_two.loop(screen)
        self.player.loop(screen)
        
