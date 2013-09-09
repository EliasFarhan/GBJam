'''
Created on 25 aout 2013

@author: efarhan
'''
import engine
from engine.init import get_screen_size
from engine.scene import Scene
from game_object.ground import Ground
from game_object.electricity import Electricity
from game_object.player import Player
from physics.physics import Physics


class GamePlay(Scene):
    def init(self):
        self.screen_size = get_screen_size()
        self.screen_pos = (0,0)
        self.physics = Physics()
        self.physics.init()
        self.player = Player(self.screen_size,self.physics)
        self.objects = [\
                        Ground(self.screen_size,(-100,-100),(120,1),self.physics),\
                        Ground(self.screen_size,(300, 0), (60,1),self.physics),\
                        Ground(self.screen_size,(600, 100), (60,1),self.physics),\
                        Electricity(self.screen_size,(700, 200),self.physics),\
                        Electricity(self.screen_size,(892, 200),self.physics),\
                        Electricity(self.screen_size,(1084, 200),self.physics),\
                        Electricity(self.screen_size,(1200, 150),self.physics,True),\
                        Electricity(self.screen_size,(800, 150),self.physics,True),\
                        Electricity(self.screen_size,(300,-20),self.physics,True),\
                        Electricity(self.screen_size,(50,30),self.physics),\
                        Electricity(self.screen_size,(100,100),self.physics,False,2),\
                        Electricity(self.screen_size,(300,200),self.physics,False,-1),\
                        Electricity(self.screen_size,(500,200),self.physics,False,1),\
                        Electricity(self.screen_size,(700,150),self.physics,False,-1),\
                        Electricity(self.screen_size,(900,200),self.physics,False,1),\
                        ]

    def loop(self, screen):
        #screen.fill(pygame.Color(255, 255, 255))
        self.physics.loop()
        for elem in self.objects:
            elem.loop(screen,self.screen_pos)
        self.screen_pos = self.player.loop(screen)
        
