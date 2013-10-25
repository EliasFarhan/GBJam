'''
Created on 23 oct. 2013

@author: efarhan
'''
import pygame
from engine.init import get_screen_size
from engine.scene import Scene
from engine.image_manager import img_manager
from game_object.game_object import GameObject
from game_object.player import Player
from physics.physics import Physics
from game_object.rpg_animation import RPGAnimation




class RPGamePlay(Scene):
    def init(self):
        self.screen_size = get_screen_size()
        self.screen_pos = (0,0)
        self.physics = Physics()
        self.physics.init(0)
        self.player = Player(self.physics)
        self.player.set_animation(RPGAnimation(img_manager, self.player.size))
        self.background = GameObject(self.physics,img_path='data/sprites/rpg_background/background.png',size=(3*480,3*320))
        self.anim_counter = 0
        pygame.mixer.init()
        if(not pygame.mixer.music.get_busy()):
            pygame.mixer.music.load('data/music/Tenchi - Mushroom City.ogg')
            pygame.mixer.music.play()
    def loop(self, screen):
        #screen.fill(pygame.Color(255, 255, 255))
        if(not pygame.mixer.music.get_busy()):
            pygame.mixer.music.play()
        self.physics.loop()
        self.background.loop(screen,self.screen_pos)
        self.screen_pos = self.player.loop(screen,self.screen_pos)
        
  
    def death(self):
        from engine.level_manager import switch
        switch('gameplay')