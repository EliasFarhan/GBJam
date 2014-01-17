'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object.image import Image
from game_object.player_export import load_player
from engine.event import get_keys
from animation.animation import Animation
from engine.const import log
from physics.physics import meter2pixel, move
from game_object import physic_object
from engine.init import get_screen_size

class Player(Image):
    def __init__(self, path, pos=(0,0),layer = 1):
        self.layer = layer
        self.filename = path
        self.anim = Animation()
        self.size = None
        self.body = None
        self.pos = pos
        self.screen_relative_pos = None
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
            move(self.body, 1)
        elif horizontal == 1:
            self.anim.state = 'move_right'
            move(self.body, -1)
        else:
            self.anim.state = 'still_right'
            move(self.body, 0)
        
        physic_pos = (meter2pixel(self.body.position[0]),meter2pixel(self.body.position[1]))
        log(physic_pos)
        pos = (physic_pos[0]-self.screen_relative_pos[0]*get_screen_size()[0],
               physic_pos[1]-self.screen_relative_pos[1]*get_screen_size()[1])
        self.pos = pos
        