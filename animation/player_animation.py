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
        self.gravity = 30.0/60
        self.direction = True #True for right
        self.jump_step = CONST.jump_step
        self.wall = 0 #None=0, Left=1, Right=2
        self.wall_speed = 2.5
        self.wall_jump_step = 0
        self.not_sliding_wall = 0

        self.attacking = 0
        self.attack_time = 30



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
        B_BUTTON = input_manager.get_button('B')
        
        horizontal = RIGHT-LEFT
        vertical = UP-DOWN
        
        physics_events = get_physics_event()
        
        for event in physics_events:

            if (event.a.userData == 2 and 15 >= event.b.userData >= 11 ) or \
                    ( event.b.userData == 2 and 15 >= event.a.userData >= 11):
                if event.begin:
                    self.foot += 1
                else:
                    self.foot -= 1
            elif (event.a.userData == 3 and event.b.userData == 11 ) or \
                    ( event.b.userData == 3  and event.a.userData == 11):
                if event.begin:
                    self.wall = 1
                else:
                    self.wall = 0

            elif (event.a.userData == 4 and event.b.userData == 11 ) or \
                    ( event.b.userData == 4  and event.a.userData == 11):
                if event.begin:
                    self.wall = 2
                else:
                    self.wall = 0
            elif (event.a.userData == 3 and 15 >= event.b.userData > 11 ) or \
                    ( event.b.userData == 3  and 15 >= event.a.userData > 11):
                log("Physics: "+str(event.a.userData)+" "+str(event.b.userData))
                if event.begin:
                    self.not_sliding_wall = 1
                else:
                    self.not_sliding_wall = 0

            elif (event.a.userData == 4 and 15 >= event.b.userData > 11 ) or \
                    ( event.b.userData == 4  and 15 >= event.a.userData > 11):
                log("Physics: "+str(event.a.userData)+" "+str(event.b.userData))
                if event.begin:
                    self.not_sliding_wall = 2
                else:
                    self.not_sliding_wall = 0
            elif (event.a.userData == 1 and event.b.userData >= 20 ) or \
                    ( event.b.userData == 1 and event.a.userData >= 20):
                log("Touched by cat")
            if (event.a.userData == 1 and event.b.userData == 13 ) or \
                    ( event.b.userData == 1 and event.a.userData == 13):
                log("Touched by spike")


        if A_BUTTON and ((self.foot and self.jump_step) or (not self.foot and self.jump_step and self.wall)):
            if self.wall == 1:
                #going RIGHT because LEFT wall
                physics_manager.move(self.player.body, vx=self.speed)
                self.wall_jump_step = CONST.wall_jump

            elif self.wall == 2:
                physics_manager.move(self.player.body, vx=-self.speed)
                self.wall_jump_step = CONST.wall_jump
            physics_manager.jump(self.player.body)
            self.jump_step -= 1
        elif not self.foot and not self.wall :
            self.jump_step = 0
        elif (self.foot or (not self.foot and self.wall)) and not A_BUTTON:
            self.jump_step = CONST.jump_step

        if B_BUTTON and self.attacking == 0:
            log("ATTACKING")
            self.attacking = self.attack_time
        elif self.attacking > 1:
            self.attacking -= 1
        elif not B_BUTTON:
            self.attacking = 0

        if horizontal == -1:
            #LEFT
            self.direction = False
            if self.foot:
                self.state = 'move'
            self.player.flip = True

            if self.wall != 1 and self.wall_jump_step == 0 and self.not_sliding_wall != 1:
                physics_manager.move(self.player.body, -self.speed)
        elif horizontal == 1:
            #RIGHT
            self.direction = True
            if self.foot:
                self.state = 'move'
            self.player.flip = False

            if self.wall != 2 and self.wall_jump_step == 0 and self.not_sliding_wall != 2:
                physics_manager.move(self.player.body, self.speed)
        else:
            if self.foot:
                if self.direction:
                    self.state = 'still'
                    self.player.flip = False
                else:
                    self.state = 'still'
                    self.player.flip = True
            if self.wall_jump_step == 0:
                physics_manager.move(self.player.body, 0)

        if not self.foot:
            if self.direction:
                self.state = 'jump'
                self.player.flip = False
            else:
                self.state = 'jump'
                self.player.flip = True


        #"gravity" effect like nes game
        velocity = physics_manager.get_body_velocity(self.player.body)
        delta = self.gravity
        if self.wall and self.wall_jump_step == 0:
            velocity.y = self.wall_speed
        else:
            velocity.y += delta
        physics_manager.set_body_velocity(self.player.body, velocity)

        physics_pos = physics_manager.get_body_position(self.player.body)
        
        if physics_pos:
            pos = physics_pos-self.player.size/2
        else:
            pos = self.player.pos
        if self.player.screen_relative_pos:
            pos = pos-self.player.screen_relative_pos*engine.get_screen_size()
        self.player.pos = pos

        self.set_screen_pos()

        if self.wall_jump_step != 0:
            self.wall_jump_step -= 1

    def set_screen_pos(self):
        level_manager.level.screen_pos = self.player.pos

    @staticmethod
    def parse_animation(anim_data):
        Animation.parse_animation(anim_data)