'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object.image import Image
from game_object.player_export import load_player

class Player(Image):
    def __init__(self, path, pos=(0,0),layer = 1):
        self.layer = 1
        self.filename = path
        load_player(self)
        self.anim.load_images()
        self.init_physics()
    def loop(self, screen, screen_pos):
        Image.loop(self, screen, screen_pos)
    def init_physics(self):
        pass
    def update_event(self):
        pass
    