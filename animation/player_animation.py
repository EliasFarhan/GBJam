'''
Created on 1 mars 2014

@author: efarhan
'''
from event.event_main import get_button
from event.physics_event import get_physics_event
from engine.physics_manager import physics_manager
from engine.init import get_screen_size
from animation.animation_main import Animation
from engine.const import log

class PlayerAnimation(Animation):
    def __init__(self,player):
        Animation.__init__(self, player)
        self.foot = 0
        self.player = self.obj
        self.speed = 3
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
            if (event.a.userData == 2 and event.b.userData == 11 ) or \
                    ( event.b.userData == 2 and event.a.userData == 11):
                if event.begin:
                    self.foot += 1
                else:
                    self.foot -= 1
        
        if horizontal == -1:
            self.direction = False
            if self.foot:
                self.state = 'move_left'
            physics_manager.move(self.player.body, -self.speed)
        elif horizontal == 1:
            self.direction = True
            if self.foot:
                self.state = 'move_right'
            physics_manager.move(self.player.body, self.speed)
        else:
            if self.foot:
                if self.direction:
                    self.state = 'still_right'
                else:
                    self.state = 'still_left'
            physics_manager.move(self.player.body, 0)
        if not self.foot:
            if self.direction:
                self.state = 'jump_right'
            else:
                self.state = 'jump_left'
        physics_pos = physics_manager.get_body_position(self.player.body)
        
        if physics_pos:
            pos = physics_pos-self.player.size/2
        else:
            pos = self.player.pos
        if self.player.screen_relative_pos:
            pos = pos-self.player.screen_relative_pos*get_screen_size()
        self.player.pos = pos

    def get_screen_pos(self):
        return self.player.pos

    @staticmethod
    def parse_animation(anim_data):
        Animation.parse_animation(anim_data)