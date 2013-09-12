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

        self.screen_pos = (0,0)
        self.physics = Physics()
        self.physics.init()
        self.player = Player(self.screen_size,self.physics,move=1)
        d1 = 2000
        d2 = 1000
        self.checkpoints = [(d2,0),(d1,0)]
        self.objects = [\
                        #first part
                        Ground(self.screen_size,(-100,-100),(10,1),self.physics),\
                        Electricity(self.screen_size,(290,-84),self.physics),\
                        Electricity(self.screen_size,(482,-84),self.physics),\
                        Electricity(self.screen_size,(674,-84),self.physics),\
                        #first part
                        Ground(self.screen_size,(d2-100,-100),(10,1),self.physics),\
                        Electricity(self.screen_size,(d2+290,-84),self.physics),\
                        Electricity(self.screen_size,(d2+400,-132),self.physics,vertical=True),\
                        Electricity(self.screen_size,(d2+700,-132),self.physics,vertical=True),\
                        Electricity(self.screen_size,(d2+600,-132),self.physics,vertical=True),\
                        Electricity(self.screen_size,(d2+482,-84),self.physics),\
                        Electricity(self.screen_size,(d2+674,-84),self.physics),\
                        #difficult part
                        Ground(self.screen_size,(-100+d1,-100),(120,1),self.physics),\
                        Ground(self.screen_size,(300+d1,0),(10,1),self.physics),\
                        Electricity(self.screen_size,(d1+316-32-128-32,16+32),self.physics),\
                        Electricity(self.screen_size,(d1+316,16),self.physics,vertical=True),\
                        Electricity(self.screen_size, (d1+400,-116), self.physics, vertical=False, turning=1),\
                        Electricity(self.screen_size, (d1+550,-116), self.physics, vertical=False, turning=-1),\
                        Electricity(self.screen_size, (d1+700,-116), self.physics, vertical=False, turning=2),\
                        Electricity(self.screen_size, (d1+850,-116), self.physics, vertical=False, turning=-2),\
                        Electricity(self.screen_size, (d1+500,150), self.physics, vertical=False, turning=3),\
                        ]

    def loop(self, screen):
        #screen.fill(pygame.Color(255, 255, 255))
        self.physics.loop()
        for elem in self.objects:
            elem.loop(screen,self.screen_pos)
        self.screen_pos = self.player.loop(screen,self.screen_pos)
        if self.player.pos[1] < -400:
            self.death()
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
        