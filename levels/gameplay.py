'''
Created on 25 aout 2013

@author: efarhan
'''
import engine
from engine.init import get_screen_size
from engine.scene import Scene
from game_object.ground import Ground
from game_object.electricity import Electricity
from game_object.fire import FireTube
from game_object.player import Player
from physics.physics import Physics



class GamePlay(Scene):
    def init(self):
        self.screen_size = get_screen_size()
        self.screen_pos = (0,0)
        self.physics = Physics()
        self.physics.init()
        self.player = Player(self.physics)
        self.objects = [\
                        Ground((-100,-100),(120,1),self.physics),\
                        Ground((300, 0), (60,1),self.physics),\
                        Ground((600, 100), (60,1),self.physics),\
                        Electricity((700, 200),self.physics),\
                        Electricity((892, 200),self.physics),\
                        Electricity((1084, 200),self.physics),\
                        Electricity((1200, 150),self.physics,True),\
                        Electricity((800, 150),self.physics,True),\
                        Electricity((300,-20),self.physics,True),\
                        Electricity((50,30),self.physics),\
                        Electricity((100,100),self.physics,False,2),\
                        Electricity((300,200),self.physics,False,-1),\
                        Electricity((500,200),self.physics,False,1),\
                        Electricity((700,150),self.physics,False,-1),\
                        Electricity((900,200),self.physics,False,1),\
                        FireTube((100,-230+16),self.physics,length=2),\
                        FireTube((200,-230+16),self.physics,length=2,begin=0),\
                        Ground((-300,-230-5*32),(120,5),self.physics),\
                        Ground((-300,-200),(3,1),self.physics),\
                        ]

    def loop(self, screen):
        #screen.fill(pygame.Color(255, 255, 255))
        self.physics.loop()
        for elem in self.objects:
            elem.loop(screen,self.screen_pos)
        self.screen_pos = self.player.loop(screen,self.screen_pos)
    def death(self):
        from engine.level_manager import switch
        switch('gameplay')
