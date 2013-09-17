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
        self.player = Player(self.physics,move=1)
        d1 = 5000
        d2 = 1000
        d3 = 2000
        d4 = 3000
        d5 = 4000
        self.checkpoints = [(d2,0),(d1,0),(d3,0),(d4,0)]
        self.objects = [\
                        #first part
                        Ground((-100,-100),(10,1),self.physics),\
                        Electricity((290,-84),self.physics),\
                        Electricity((482,-84),self.physics),\
                        Electricity((674,-84),self.physics),\
                        #second part
                        Ground((d2-100,-100),(10,1),self.physics),\
                        Electricity((d2+290,-84),self.physics),\
                        Electricity((d2+400,-132),self.physics,vertical=True),\
                        Electricity((d2+700,-132),self.physics,vertical=True),\
                        Electricity((d2+600,-132),self.physics,vertical=True),\
                        Electricity((d2+482,-84),self.physics),\
                        Electricity((d2+674,-84),self.physics),\
                        #third part
                        Ground((d3-100,-100),(10,1),self.physics),\
                        Electricity((d3+290,-84),self.physics),\
                        Electricity((d3+482,-84),self.physics),\
                        Electricity((d3+674,-84),self.physics),\
                        Electricity((d3+500,0),self.physics,turning=1),\
                        Electricity((d3+700,0),self.physics,turning=-1),\
                        #fourth part
                        Ground((d4-100,-100),(10,1),self.physics),\
                        Electricity((d4+290,-84),self.physics),\
                        Electricity((d4+482,-84),self.physics),\
                        Electricity((d4+674,-84),self.physics),\
                        Electricity((d4+500,0),self.physics,turning=1),\
                        Electricity((d4+700,0),self.physics,turning=-2),\
                        Electricity((d4+400,-132),self.physics,vertical=True),\
                        Electricity((d4+700,-132),self.physics,vertical=True),\
                        Electricity((d4+600,-132),self.physics,vertical=True),\
                        #fifth part
                        Ground((d5-100,-100),(25,1),self.physics),\
                        Ground((d5+300,0),(10,1),self.physics),\
                        Ground((d5+300,32),(1,10),self.physics),\
                        Electricity( (d5+400,-116), self.physics, vertical=False, turning=1),\
                        Electricity( (d5+550,-116), self.physics, vertical=False, turning=-1),\
                        #sixth part
                        Ground((-100+d1,-100),(120,1),self.physics),\
                        Ground((300+d1,0),(10,1),self.physics),\
                        Electricity((d1+316-32-128-32,16+32),self.physics),\
                        Electricity((d1+316,16),self.physics,vertical=True),\
                        Electricity( (d1+400,-116), self.physics, vertical=False, turning=1),\
                        Electricity( (d1+550,-116), self.physics, vertical=False, turning=-1),\
                        Electricity( (d1+700,-116), self.physics, vertical=False, turning=2),\
                        Electricity( (d1+850,-116), self.physics, vertical=False, turning=-2),\
                        Electricity( (d1+500,150), self.physics, vertical=False, turning=3),\
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
        