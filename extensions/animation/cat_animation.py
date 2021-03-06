from animation.animation_main import Animation
from animation.player_animation import PlayerAnimation
from engine import level_manager
from engine.const import log, CONST
from engine.init import engine
from engine.vector import Vector2
from event.physics_event import physics_events
from extensions.game_object.bullet import Bullet
from levels.gamestate import GameState
from physics_engine.physics_manager import physics_manager
from render_engine.snd_manager import snd_manager

__author__ = 'Elias'

class CatAnimation(PlayerAnimation):
    def __init__(self,object):
        Animation.__init__(self,object)
        self.obj = object
        self.img = None
        self.nmb = 0
        self.in_area_left = False
        self.in_area_right = False
        if isinstance(level_manager.level, GameState):
            self.player = level_manager.level.player
        self.active = False
        self.bullets = []
        self.bullet_frequency = 90
        self.bullet_time = 0
        self.current_bullet = 0
        self.shoot_sound = snd_manager.load_sound("data/sound/Shot1.wav")
        self.direction = -1#-1 left, 1 right
        self.death = -1


    def update_animation(self, state="", invert=False,lock=False):
        self.update_state()
        Animation.update_animation(self)

    def update_state(self):
        if not self.obj.move:
            self.anim_freq = 2
        if self.nmb == 0:
            self.nmb = self.obj.body.fixtures[0].userData
            self.current_bullet = self.nmb + 1

        player_pos = level_manager.level.player.pos + level_manager.level.player.screen_relative_pos*engine.screen_size
        if self.obj.pos.x+engine.screen_size.x > player_pos.x > self.obj.pos.x-engine.screen_size.x:
            self.active = True
        else:
            self.active = False

        if self.active and not self.obj.move and self.death == -1:
            if self.bullet_time == 0:
                snd_manager.play_sound(self.shoot_sound)
                self.state = 'attack'
                self.bullets.append(Bullet(
                                            pos=self.obj.pos+Vector2(-10,17),
                                            size=Vector2(16,16),
                                            userData=self.current_bullet,
                                            speed=Vector2(self.direction*5,0)))
                self.current_bullet += 1
                if self.current_bullet == self.nmb + 10:
                    self.current_bullet = self.nmb + 1
                self.bullet_time = self.bullet_frequency
            else:
                self.bullet_time -= 1
                if self.state == 'attack' and self.bullet_time < self.bullet_frequency-3*self.anim_freq:
                    self.state = 'still'
            remove_bullet = []
            for b in self.bullets:
                b.loop(engine.screen)
                if not (b.pos.x+engine.screen_size.x > player_pos.x > b.pos.x-engine.screen_size.x):
                    remove_bullet.append(b)
            for b in remove_bullet:
                self.bullets.remove(b)
            del remove_bullet[:]


        if self.death == -1:
            self.obj.pos = physics_manager.get_body_position(self.obj.body)-self.obj.size/2






        for event in physics_events:
            if ((event.a.userData == 5 and event.b.userData == self.nmb) or\
                    (event.b.userData == 5 and event.a.userData == self.nmb)):

                self.in_area_left = event.begin
            elif (event.b.userData == 6 and event.a.userData == self.nmb) or\
                    (event.a.userData == 6 and event.b.userData == self.nmb):
                self.in_area_right = event.begin
            elif self.obj.move and (( 15 > event.a.userData >= 11 and event.b.userData == self.nmb) or\
                ( 15 > event.b.userData >= 11 and event.a.userData == self.nmb)):
                if event.begin:
                    self.direction = - self.direction

        if self.obj.move and self.death == -1:
            physics_manager.move(self.obj.body, vx=self.direction*3)
            self.state = 'move'

        if self.direction == -1:
            self.obj.flip = True
        else:
            self.obj.flip = False

        if self.death == -1:
            if self.in_area_left:
                if not self.player.anim.direction and self.player.anim.attacking>1:
                    self.death = 60
                    physics_manager.remove_body(self.obj.body)
            if self.in_area_right:
                if self.player.anim.direction and self.player.anim.attacking > 1:
                    self.death = 60
                    physics_manager.remove_body(self.obj.body)

        if self.death > 0:
            self.state = 'hit'
            self.death -= 1
            if self.death % 20 > 10:
                self.obj.show = False
            else:
                self.obj.show = True


        if self.death == 0:
            self.obj.remove = True