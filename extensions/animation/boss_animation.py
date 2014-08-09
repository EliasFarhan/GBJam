from engine.init import engine
from engine.stat import set_value, get_value
from engine.vector import Vector2
from render_engine.img_manager import img_manager
from render_engine.input import input_manager
from render_engine.snd_manager import snd_manager

__author__ = 'efarhan'

from animation.animation_main import Animation
from animation.player_animation import PlayerAnimation
from engine import level_manager
from levels.gamestate import GameState
from physics_engine.physics_manager import physics_manager

__author__ = 'Elias'

class BossAnimation(PlayerAnimation):
    def __init__(self,object):
        Animation.__init__(self,object)
        self.obj = object
        self.img = None
        self.dialog = False
        self.nmb = 0
        self.in_area_left = False
        self.in_area_right = False
        self.boss_img = img_manager.load_image("data/sprites/boss/Bosscat.png")
        self.boss_delta = Vector2(60,10)
        self.animation_delta = Vector2()
        if isinstance(level_manager.level, GameState):
            self.player = level_manager.level.player

        self.boss_fight = False

        self.state = 'idle'
        self.direction = 0


    def update_animation(self, state="", invert=False,lock=False):
        self.update_state()
        Animation.update_animation(self)

    def update_state(self):

        player_pos = self.player.pos + self.player.screen_relative_pos * engine.screen_size

        if player_pos.x > 250 and not self.dialog:
            snd_manager.set_playlist(["data/music/intro_BOSS1_gbjam.ogg","data/music/BOSS1_gbjam.ogg"])
            self.dialog = True
            engine.show_dialog = 1
            engine.textbox.set_text("Kitler", "We meet again, Fury")
            level_manager.level.lock = True
        if self.dialog == 1 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                engine.textbox.set_text("Fury", "This time, you will lose more than one eye")
                self.dialog = 2
        if self.dialog == 2 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                engine.textbox.set_text("Kitler", "I won't, I have a panzer now")
                self.dialog = 3
        if not self.boss_fight and self.dialog == 3 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.boss_fight = True
                self.direction = 1
                engine.show_dialog = False
                level_manager.level.lock = False
        if self.boss_fight:
            self.state = 'backward'

            set_value("boss_limit", [50,595])

        if self.state == 'idle' or self.state == 'forward' or self.state == 'backward':
            if self.index == 0 or self.index == 4 or self.index == 5:
                self.animation_delta = Vector2(0,0)
            elif self.index == 2 or self.index == 3:
                self.animation_delta = Vector2(0,2)
            elif self.index == 1:
                self.animation_delta = Vector2(0,1)

        self.obj.pos = physics_manager.get_body_position(self.obj.body)-self.obj.size/2
        img_manager.show_image(self.boss_img, engine.screen, self.obj.pos-level_manager.level.screen_pos+self.boss_delta+self.animation_delta)

        if self.state == 'backward' or self.state == 'forward':
            physics_manager.move(self.obj.body,vx=self.direction*2.5)

        if self.boss_fight:
            if self.direction == -1 and (self.obj.pos+self.obj.size).x<get_value('boss_limit')[0]:
                self.state = 'backward'
                self.direction = 1
            elif self.direction == 1 and self.obj.pos.x > get_value('boss_limit')[1]:
                self.state = 'forward'
                self.direction = -1
