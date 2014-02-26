'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object.image import Image, AnimImage
from json_export.player_json import load_player
from animation.animation import Animation
from engine.const import log,pookoo
from engine.physics import meter2pixel, move
from game_object import physic_object
from engine.init import get_screen_size
from event.keyboard_event import get_button
from event.physics_event import get_physics_event
if pookoo:
    import physics

class Player(AnimImage):
    def __init__(self, path, pos=(0,0),layer = 1):
        self.layer = layer
        self.filename = path
        self.anim = Animation()
        self.body = None
        self.foot = False
        self.center_image = True
        self.direction = True #True for right
        log('Loading player file '+self.filename)
        status = load_player(self)
        if status != 1:
            log("Error while loading player "+str(status))
            return
        self.init_image()
    def init_image(self):
        self.anim.load_images(size=self.size,permanent=True)

    def loop(self, screen, screen_pos,editor=False):
        if not editor:
            self.update_event()
        AnimImage.loop(self, screen, screen_pos)
        return self.pos

    def update_event(self):
        
        RIGHT = get_button('player_right')
        LEFT = get_button('player_left')
        UP = get_button('player_up')
        DOWN = get_button('player_down')
        
        horizontal = RIGHT-LEFT
        vertical = UP-DOWN
        
        physics_events = get_physics_event()
        
        for event in physics_events:
            if event.a == 2 or event.b == 2:
                self.foot = event.begin
        
        if horizontal == -1:
            self.direction = False
            if self.foot:
                self.anim.state = 'move_left'
            move(self.body, -1)
        elif horizontal == 1:
            self.direction = True
            if self.foot:
                self.anim.state = 'move_right'
            move(self.body, 1)
        else:
            if self.foot:
                if self.direction:
                    self.anim.state = 'still_right'
                else:
                    self.anim.state = 'still_left'
            move(self.body, 0)
        if not self.foot:
            if self.direction:
                self.anim.state = 'jump_right'
            else:
                self.anim.state = 'jump_left'
        physics_pos = (0,0)
        if not pookoo:
            physics_pos = self.body.position
        else:
            physics_pos = physics.body_get_position(self.body)
        physics_pos = (meter2pixel(physics_pos[0]),meter2pixel(physics_pos[1]))
        pos = (physics_pos[0]-self.screen_relative_pos[0]*get_screen_size()[0],
               physics_pos[1]-self.screen_relative_pos[1]*get_screen_size()[1])
        self.pos = pos
        