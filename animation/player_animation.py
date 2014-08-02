'''
Created on 1 mars 2014

@author: efarhan
'''
from engine import level_manager
from engine.const import CONST, log
from engine.vector import Vector2
from render_engine.input import input_manager

from event.physics_event import get_physics_event
from engine.init import engine
from animation.animation_main import Animation
from physics_engine.physics_manager import physics_manager


class PlayerAnimation(Animation):
    def __init__(self,player):
        Animation.__init__(self, player)
        self.foot = 0
        self.player = self.obj
        self.speed = 3
        self.direction = True #True for right
        self.jump_step = CONST.jump_step

    def load_images(self, size=None, tmp=False):
        Animation.load_images(self, size=size, tmp=tmp)
    
    def update_animation(self, state="", invert=False):
        self.update_state()
        return Animation.update_animation(self, state=state, invert=invert)

    def update_state(self):
        RIGHT = input_manager.get_button('RIGHT')
        LEFT = input_manager.get_button('LEFT')
        UP = input_manager.get_button('UP')
        DOWN = input_manager.get_button('DOWN')
        A_BUTTON = input_manager.get_button('A')
        
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

        if A_BUTTON and self.foot and self.jump_step:
            physics_manager.jump(self.player.body)
            self.jump_step -= 1
        elif not self.foot:
            self.jump_step = 0
        elif (self.foot and not A_BUTTON):
            self.jump_step = CONST.jump_step

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
                self.state = 'jump'
                self.player.flip = True

        physics_pos = physics_manager.get_body_position(self.player.body)
        
        if physics_pos:
            pos = physics_pos-self.player.size/2
        else:
            pos = self.player.pos
        if self.player.screen_relative_pos:
            pos = pos-self.player.screen_relative_pos*engine.get_screen_size()
        self.player.pos = pos

        self.set_screen_pos()

    def set_screen_pos(self):
        level_manager.level.screen_pos = Vector2(self.player.pos.x,0)

    @staticmethod
    def parse_animation(anim_data):
        Animation.parse_animation(anim_data)