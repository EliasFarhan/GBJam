'''
Created on 11 janv. 2014

@author: efarhan
'''
from engine.scene import Scene


class MenuState(Scene):
    def __init__(self):
        Scene.__init__(self)
    def init(self):
        Scene.init(self)
    def loop(self, screen):
        Scene.loop(self, screen)
    def exit(self, screen):
        Scene.exit(self, screen)