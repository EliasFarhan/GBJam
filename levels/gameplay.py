'''
Created on 9 dec. 2013

@author: efarhan
'''
import pygame
from engine.init import get_screen_size
from engine.scene import Scene
from engine.const import framerate

from game_object.player import Player
from levels.level_export import load_level

class GamePlay(Scene):
    def __init__(self,filename):
        self.filename = filename
        self.init()
    def init(self):
        self.editor = False
        
        self.images = [
                       [],#Layer 5
                       [],#Layer 4
                       [],#Layer 3
                       [],#Layer 2
                       [],#Layer 1
                       
                       ]
        self.physics_objects = [
                                ]
        self.screen_pos = (0,0)
        if self.filename != "":
            load_level(self)
        
    def reload(self,newfilename):
        self.filename = newfilename
        self.init()
    def loop(self, screen):
        for i in range(self.player.layer):
            for j in len(self.images[i]):
                pass
        self.player.loop(screen,self.screen_pos)
        for i in range(self.player.layer,len(self.images)):
            for j in len(self.images[i]):
                pass
        for physic_object in self.physics_objects:
            pass
    def exit(self, screen):
        Scene.exit(self, screen)

'''Editor functions'''
def save_level(self):
    pass