'''
Created on 25 aout 2013

@author: efarhan
'''
import engine
from engine.init import get_screen_size
from engine.scene import Scene
from engine.game_object import GameObject,Player, Ground,Electricity
from physics.physics import Physics, set_ratio_pixel
import pygame


class GamePlay(Scene):
    def init(self):
        screen_size = get_screen_size()
        self.screen_pos = (0,0)
        self.physics = Physics()
        self.physics.init()
        self.player = Player(screen_size,self.physics)
        self.ground = Ground(screen_size,(-100,-100),120,self.physics)
        self.floor_one = Ground(screen_size,(300, 0), 60,self.physics)
        self.floor_two = Ground(screen_size,(600, 100), 60,self.physics)
        self.electricity = Electricity(screen_size,(700, 200),self.physics)

    def loop(self, screen):
        #screen.fill(pygame.Color(255, 255, 255))
        self.physics.loop()
        self.electricity.loop(screen,self.screen_pos)
        self.ground.loop(screen,self.screen_pos)
        self.floor_one.loop(screen,self.screen_pos)
        self.floor_two.loop(screen,self.screen_pos)
        self.screen_pos = self.player.loop(screen)
        
