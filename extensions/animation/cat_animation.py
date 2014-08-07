from animation.animation_main import Animation
from animation.player_animation import PlayerAnimation
from engine import level_manager
from engine.const import log
from event.physics_event import physics_events
from levels.gamestate import GameState
from physics_engine.physics_manager import physics_manager

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
    


    def update_animation(self, state="", invert=False,lock=False):
        self.update_state()
        Animation.update_animation(self)

    def update_state(self):
        self.state = 'still'
        if self.nmb == 0:
            self.nmb = self.obj.body.fixtures[0].userData


        for event in physics_events:
            if ((event.a.userData == 5 and event.b.userData == self.nmb) or\
                    (event.b.userData == 5 and event.a.userData == self.nmb)):

                self.in_area_left = event.begin
            elif (event.b.userData == 6 and event.a.userData == self.nmb) or\
                    (event.a.userData == 6 and event.b.userData == self.nmb):
                self.in_area_right = event.begin
        if self.in_area_left:
            if not self.player.anim.direction and self.player.anim.attacking>1:
                self.obj.remove = True
        if self.in_area_right:
            if self.player.anim.direction and self.player.anim.attacking > 1:
                self.obj.remove = True
        if self.obj.remove:
            physics_manager.remove_body(self.obj.body)
    @staticmethod
    def parse_animation(anim_data):
        return CatAnimation(None)