'''
Created on 9 dec. 2013

@author: efarhan
'''
import pygame
from engine.init import get_screen_size
from engine.scene import Scene
from engine.const import framerate, log

from game_object.player import Player
from levels.level_export import load_level
from physics.physics import init_physics


class GamePlay(Scene):
    def __init__(self,filename):
        self.filename = filename
    def init(self):
        init_physics()
        self.editor = False
        
        self.images = [
                       [],#Layer 5
                       [],#Layer 4
                       [],#Layer 3
                       [],#Layer 2
                       [],#Layer 1
                       
                       ]
        self.physic_objects = [
                                ]
        self.screen_pos = (0,0)
        if self.filename != "":
            log("Loading level "+self.filename)
            if not load_level(self):
                from engine.level_manager import switch_level
                switch_level(Scene())
        
        
        
    def reload(self,newfilename):
        self.filename = newfilename
        self.init()
    def loop(self, screen):
        for i in range(self.player.layer):
            for j in range(len(self.images[i])):
                pass
        self.player.loop(screen,self.screen_pos)
        for i in range(self.player.layer,len(self.images)):
            for j in range(len(self.images[i])):
                pass
        for physic_object in self.physic_objects:
            physic_object.loop(screen,self.screen_pos)
    def exit(self, screen):
        Scene.exit(self, screen)

'''Editor functions'''
def save_level(self):
    pass