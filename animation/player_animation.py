'''
Created on 1 mars 2014

@author: efarhan
'''
from engine.input import input_manager

from event.physics_event import get_physics_event
from engine.physics_manager import physics_manager
from engine.init import engine
from animation.animation_main import Animation
from engine.const import log

class PlayerAnimation(Animation):
    def __init__(self,player):
        Animation.__init__(self, player)
        self.foot = 0
        self.player = self.obj
        self.speed = 3
        self.direction = True #True for right

    def load_images(self, size=None, tmp=False):
        Animation.load_images(self, size=size, tmp=tmp)
    
    def update_animation(self, state="", invert=False):
        self.update_state()
        return Animation.update_animation(self, state=state, invert=invert)

    def update_state(self):
        RIGHT = input_manager.get_button('player_right')
        LEFT = input_manager.get_button('player_left')
        UP = input_manager.get_button('player_up')
        DOWN = input_manager.get_button('player_down')
        
        horizontal = RIGHT-LEFT
        vertical = UP-DOWN
        
        physics_events = get_physics_event()
        
        for event in physics_events:
            if (event.a.userData == 2 and event.b.userData == 11 ) or \
                    ( event.b.userData == 2 and event.a.userData == 11):
                if event.begin:
                    self.foot += 1
                else:
                    self.foot -= 1
        
        if horizontal == -1:
            self.direction = False
            if self.foot:
                self.state = 'move'
            self.player.flip = True
            physics_manager.move(self.player.body, -self.speed)
        elif horizontal == 1:
            self.direction = True
            if self.foot:
                self.state = 'move'
            self.player.flip = False
            physics_manager.move(self.player.body, self.speed)
        else:
            if self.foot:
                if self.direction:
                    self.state = 'still'
                    self.player.flip = False
                else:
                    self.state = 'still'
                    self.player.flip = True
            physics_manager.move(self.player.body, 0)
        if not self.foot:
            if self.direction:
                self.state = 'jump'
                self.player.flip = False
            else:
                self.state = 'jump_left'
                self.player.flip = True
        physics_pos = physics_manager.get_body_position(self.player.body)
        
        if physics_pos:
            pos = physics_pos-self.player.size/2
        else:
            pos = self.player.pos
        if self.player.screen_relative_pos:
            pos = pos-self.player.screen_relative_pos*engine.get_screen_size()
        self.player.pos = pos

    def get_screen_pos(self):
        return self.player.pos

    @staticmethod
    def parse_animation(anim_data):
        Animation.parse_animation(anim_data)