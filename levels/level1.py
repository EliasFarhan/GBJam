'''
Created on 9 sept. 2013

@author: efarhan
'''

from levels.gameplay import GamePlay
from game_object.ground import Ground
from game_object.player import Player
from game_object.electricity import Electricity
from physics.physics import Physics
from engine.init import get_screen_size
from engine.event import get_retry


class Level1(GamePlay):
    def init(self):
        self.screen_size = get_screen_size()
        self.checkpoints = [(1000,0)]
        self.screen_pos = (0,0)
        self.physics = Physics()
        self.physics.init()
        self.player = Player(self.screen_size,self.physics,move=1)
        self.objects = [\
                        Ground(self.screen_size,(-100,-100),(120,1),self.physics),\
                        Ground(self.screen_size,(300,0),(10,1),self.physics),\
                        Electricity(self.screen_size,(316-32-128-32,16+32),self.physics),\
                        Electricity(self.screen_size,(316,16),self.physics,vertical=True),\
                        Electricity(self.screen_size, (400,-116), self.physics, vertical=False, turning=1),\
                        Electricity(self.screen_size, (550,-116), self.physics, vertical=False, turning=-1),\
                        Electricity(self.screen_size, (700,-116), self.physics, vertical=False, turning=2),\
                        Electricity(self.screen_size, (850,-116), self.physics, vertical=False, turning=-2),\
                        Electricity(self.screen_size, (500,150), self.physics, vertical=False, turning=3),\
                        Electricity(self.screen_size, (1200,-116), self.physics, vertical=False, turning=3)
                        ]

    def loop(self, screen):
        #screen.fill(pygame.Color(255, 255, 255))
        self.physics.loop()
        for elem in self.objects:
            elem.loop(screen,self.screen_pos)
        self.screen_pos = self.player.loop(screen)
        if get_retry():
            from engine.level_manager import switch
            switch('level1')
    def death(self):
        new_point = (0,0)
        for point in self.checkpoints:
            if(point[0]<self.player.pos[0] and point[0]>new_point[0]):
                new_point = point
        self.player.set_position(new_point)
        self.player.life = 100
        