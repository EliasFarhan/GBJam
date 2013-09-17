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
        pygame.mixer.init()
        pygame.mixer.music.load('data/music/Tenchi - Shriving Sorrow.ogg')
        pygame.mixer.music.play()
        self.screen_size = get_screen_size()
        self.physics = Physics()
        self.physics.init(gravity_arg=0)
        self.screen_pos = (0,0)
        self.factor = self.screen_size[1]/200
        self.player = Player( self.physics, move=-1,jump=0,factor=self.factor)

    
        nmb = 10
        
        self.boy = Image('boy/', (self.screen_size[0]/2,-self.screen_size[1]/2), (42,48), self.factor)
        self.girl = Image('girl/',(self.screen_size[0]/2,-self.screen_size[1]/2),(42,48),self.factor)
                       
    def loop(self, screen):
        #if(not pygame.mixer.music.get_busy()):
        #    from engine.level_manager import switch
        #    switch(0)
        Scene.loop(self, screen)
        screen.fill(pygame.Color(255, 255, 255))
        self.physics.loop()
        #modify such that the player is not in the center of the scene, but in the end
        zoom = self.screen_size[0]/(self.boy.pos[0]-self.player.pos[0])
        boy_pos = (self.factor*self.boy.size[0]*zoom,-self.factor*self.boy.size[1]*zoom)
        self.boy.loop(screen, (self.boy.size[0]/2*zoom,-self.boy.size[1]/2*zoom), new_size=zoom)
        self.girl.loop(screen, (self.boy.size[0]*zoom+self.girl.size[0]/2*zoom,-self.boy.size[1]*zoom+self.girl.size[1]/2*zoom), new_size=zoom)
        player_pos = self.player.loop(screen,self.screen_pos,new_size=zoom)
        self.screen_pos = (player_pos[0]+self.screen_size[0]/2-(self.player.box_size[0]+5*self.factor)*zoom,self.screen_size[1]/2-self.player.box_size[1]*zoom)
        if self.player.pos[1] < -400:
            self.death()
    def death(self):
        pass