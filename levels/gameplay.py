'''
Created on 25 aout 2013

@author: efarhan
'''
import pygame
from engine.init import get_screen_size
from engine.scene import Scene
from game_object.ground import Ground
from game_object.electricity import Electricity
from game_object.fire import FireTube, FireBall
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
                        Ground((-100,-100),(100,1),self.physics),\
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
                        FireBall((400,-100), self.physics,speed=-10),\
                        Ground((-300,-230-3*32),(120,3),self.physics),\
                        Ground((-300,-200),(3,1),self.physics),\
                        Ground((-300,-200+32),(1,4),self.physics),\
                        Ground((-300+32*120,-200+32),(1,4),self.physics),\
                        Ground((-300+32*115,-200),(5,1),self.physics),\
                        ]
        pygame.mixer.init()
        if(not pygame.mixer.music.get_busy()):
            pygame.mixer.music.load('data/music/Tenchi - Mushroom City.ogg')
            pygame.mixer.music.play()
    def loop(self, screen):
        #screen.fill(pygame.Color(255, 255, 255))
        if(not pygame.mixer.music.get_busy()):
            pygame.mixer.music.play()
        self.physics.loop()
        for elem in self.objects:
            elem.loop(screen,self.screen_pos)
        self.screen_pos = self.player.loop(screen,self.screen_pos)
    def death(self):
        from engine.level_manager import switch
        switch('gameplay')
