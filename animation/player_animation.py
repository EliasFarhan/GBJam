'''
Created on 1 mars 2014

@author: efarhan
'''
from event.physics_event import get_physics_event
from engine.physics import move, meter2pixel, get_body_position
from engine.init import get_screen_size
from event.keyboard_event import get_button
from animation.animation_main import Animation
from engine.const import log

class PlayerAnimation(Animation):
    def __init__(self,player):
        Animation.__init__(self, player)
        self.foot = False
        self.player = self.obj
        self.direction = True #True for right
    def load_images(self, size=None, permanent=False):
        Animation.load_images(self, size=size, permanent=permanent)
    
    def update_animation(self, state="", invert=False):
        self.update_state()
        return Animation.update_animation(self, state=state, invert=invert)
    def update_state(self):
        RIGHT = get_button('player_right')
        LEFT = get_button('player_left')
        UP = get_button('player_up')
        DOWN = get_button('player_down')
        
        horizontal = RIGHT-LEFT
        vertical = UP-DOWN
        
        physics_events = get_physics_event()
        
        for event in physics_events:
            if event.a.userData == 2 or event.b.userData == 2:
                self.foot = event.begin
        
        if horizontal == -1:
            self.direction = False
            if self.foot:
                self.state = 'move_left'
            move(self.player.body, -self.player.speed)
        elif horizontal == 1:
            self.direction = True
            if self.foot:
                self.state = 'move_right'
            move(self.player.body, self.player.speed)
        else:
            if self.foot:
                if self.direction:
                    self.state = 'still_right'
                else:
                    self.state = 'still_left'
            move(self.player.body, 0)
        if not self.foot:
            if self.direction:
                self.state = 'jump_right'
            else:
                self.state = 'jump_left'
        physics_pos = get_body_position(self.player.body)
        
        if physics_pos:
            pos = (physics_pos[0],
                   physics_pos[1])
        else:
            pos = (self.player.pos[0],self.player.pos[1])
        self.player.pos = pos
        log(str(pos))
    @staticmethod
    def parse_animation(anim_data):
        Animation.parse_animation(anim_data)