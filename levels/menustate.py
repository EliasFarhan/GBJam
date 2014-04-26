'''
Created on 11 janv. 2014

@author: efarhan
'''
from engine.const import enum
from levels.scene import Scene

State = enum('MAIN', 'OPTIONS', 'GRAPHICS', 'SOUNDS', 'KEYS')


class MenuState(Scene):
    def __init__(self):
        Scene.__init__(self)
        self.state = None

    def init(self):
        Scene.init(self)
        self.state = State.MAIN

    def loop(self, screen):
        Scene.loop(self, screen)


    def exit(self, screen):
        Scene.exit(self, screen)