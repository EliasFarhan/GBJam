'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object.image import Image
from game_object.player_export import load_player
from engine.event import get_keys
from animation.animation import Animation
from engine.const import log

class Player(Image):
    def __init__(self, path, pos=(0,0),layer = 1):
        self.layer = layer
        self.filename = path
        self.anim = Animation()
        self.size = None
        self.pos = pos
        log('Loading player file '+self.filename)
        status = load_player(self)
        if status != 1:
            log("Error while loading player "+str(status))
            return
        self.anim.load_images(self.size)


        
    def loop(self, screen, screen_pos):
        self.update_event()
        Image.loop(self, screen, screen_pos)
        return self.pos

    def update_event(self):

        RIGHT,LEFT,UP,DOWN,ACTION = get_keys()
        
        horizontal = RIGHT-LEFT
        vertical = UP-DOWN
        
        if horizontal == -1:
            self.anim.state = 'move_left'
        elif horizontal == 1:
            self.anim.state = 'move_right'
        else:
            self.anim.state = 'still_right'
    