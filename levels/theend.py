'''
Created on 11 sept. 2013

@author: efarhan
'''
import pygame
from engine.scene import Scene
from game_object.player import Player
from game_object.ground import Ground
from game_object.image import Image
from physics.physics import Physics
from engine.init import get_screen_size
class TheEnd(Scene):
    def init(self):
        Scene.init(self)
        self.screen_size = get_screen_size()
        self.physics = Physics()
        self.physics.init()
        self.screen_pos = (0,0)
        self.player = Player(self.screen_size, self.physics, move=-1,jump=0,factor=self.screen_size[1]/120)
        self.objects = [
                       Ground((-self.screen_size[0]*5,-self.screen_size[1]/2), (int(self.screen_size[0]*6/32),1), self.physics,factor=self.screen_size[1]/240),\
                       Image('boy/', (self.screen_size[1]/2,0), (42,48), self.screen_size[1]/120)
                       ]
    def loop(self, screen):
        Scene.loop(self, screen)
        screen.fill(pygame.Color(255, 255, 255))
        self.physics.loop()
        for elem in self.objects:
            elem.loop(screen,self.screen_pos)
        #modify such that the player is not in the center of the scene, but in the end
        player_pos = self.player.loop(screen,self.screen_pos,new_size=1)
        self.screen_pos = (player_pos[0]+self.screen_size[0]/2-self.player.size[0]/2,0)
        if self.player.pos[1] < -400:
            self.death()
    def death(self):
        pass