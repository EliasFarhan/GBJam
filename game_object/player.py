'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object.image import Image

class Player(Image):
    def __init__(self, path, pos):
        Image.__init__(self, path, pos)
        self.init_physics()
    def loop(self, screen, screen_pos):
        Image.loop(self, screen, screen_pos)
    def init_physics(self):
        pass
    def update_event(self):
        pass
    