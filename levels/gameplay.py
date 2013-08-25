'''
Created on 25 aout 2013

@author: efarhan
'''
from engine.scene import Scene
from engine.game_object import Player
import pygame
class GamePlay(Scene):
    def init(self):
        self.player = Player()
    def loop(self, screen):
        self.player.loop(screen)