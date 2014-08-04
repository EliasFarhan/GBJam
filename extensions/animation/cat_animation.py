from animation.player_animation import PlayerAnimation
from engine import level_manager
from engine.const import log
from event.physics_event import physics_events
from levels.gamestate import GameState
from physics_engine.physics_manager import physics_manager

__author__ = 'Elias'

class CatAnimation(PlayerAnimation):
    def __init__(self,object):
        self.obj = object
        self.img = None
        self.nmb = 0
        if isinstance(level_manager.level, GameState):
            self.player = level_manager.level.player
    
    def load_images(self, size=None, tmp=False):
        pass

    def update_animation(self, state="", invert=False):
        self.update_state()

    def update_state(self):
        if self.nmb == 0:
            self.nmb = self.obj.body.fixtures[0].userData


        for event in physics_events:
            if ((event.a.userData == 5 and not self.player.anim.direction and self.player.anim.attacking>1) or \
                (event.a.userData == 6 and self.player.anim.direction and self.player.anim.attacking>1)) \
                and event.b.userData == self.nmb:
                log("Death from a: "+str(event.a.userData)+" b: "+str(event.b.userData))
                self.obj.remove = True

                break
            elif ((event.b.userData == 5 and not self.player.anim.direction and self.player.anim.attacking > 1) or \
                (event.b.userData == 6 and self.player.anim.direction and self.player.anim.attacking > 1)) \
                and event.a.userData == self.nmb:
                log("Death from a: "+str(event.a.userData)+" b: "+str(event.b.userData))
                self.obj.remove = True
                break
        if self.obj.remove:
            physics_manager.remove_body(self.obj.body)
    @staticmethod
    def parse_animation(anim_data):
        return CatAnimation(None)