from engine.init import engine
from engine.vector import Vector2
from render_engine.img_manager import img_manager

__author__ = 'efarhan'

from animation.animation_main import Animation
from animation.player_animation import PlayerAnimation
from engine import level_manager
from engine.const import log
from event.physics_event import physics_events
from levels.gamestate import GameState
from physics_engine.physics_manager import physics_manager

__author__ = 'Elias'

class BossAnimation(PlayerAnimation):
    def __init__(self,object):
        Animation.__init__(self,object)
        self.obj = object
        self.img = None
        self.nmb = 0
        self.in_area_left = False
        self.in_area_right = False
        self.boss_img = img_manager.load_image("data/sprites/boss/Bosscat.png")
        self.boss_delta = Vector2(60,10)
        self.animation_delta = Vector2()
        if isinstance(level_manager.level, GameState):
            self.player = level_manager.level.player

        self.boss_fight = False



    def update_animation(self, state="", invert=False,lock=False):
        self.update_state()
        Animation.update_animation(self)

    def update_state(self):

        player_pos = self.player.pos + self.player.screen_relative_pos * engine.screen_size

        if player_pos.x > 250:
            self.boss_fight = True

        if self.state == 'idle' or self.state == 'forward' or self.state == 'backward':
            if self.index == 0 or self.index == 4 or self.index == 5:
                self.animation_delta = Vector2(0,0)
            elif self.index == 2 or self.index == 3:
                self.animation_delta = Vector2(0,2)
            elif self.index == 1:
                self.animation_delta = Vector2(0,1)

        self.obj.pos = physics_manager.get_body_position(self.obj.body)-self.obj.size/2
        img_manager.show_image(self.boss_img, engine.screen, self.obj.pos-level_manager.level.screen_pos+self.boss_delta+self.animation_delta)

        if self.boss_fight:
            if self.obj.pos.x > player_pos.x > self.obj.pos.x-engine.screen_size.x and (self.obj.pos+self.obj.size).x<700:
                self.state = 'backward'
                physics_manager.move(self.obj.body,vx=2.5)
            elif self.obj.pos.x+engine.screen_size.x > player_pos.x > self.obj.pos.x and self.obj.pos.x > 0:
                self.state = 'forward'
                physics_manager.move(self.obj.body,vx=-2.5)
            else:
                self.state = 'idle'
                physics_manager.move(self.obj.body,vx=0)
