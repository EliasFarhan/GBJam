from render_engine.img_manager import img_manager

__author__ = 'Elias'
__author__ = 'efarhan'

from animation.animation_main import Animation
from animation.player_animation import PlayerAnimation
from engine import level_manager
from engine.const import log
from event.physics_event import physics_events
from levels.gamestate import GameState
from physics_engine.physics_manager import physics_manager

__author__ = 'Elias'


class BulletAnimation(PlayerAnimation):
    def __init__(self,object):
        Animation.__init__(self,object)
        self.obj = object
        self.img = img_manager.load_image("data/sprites/bullet.png")
        self.nmb = 0
        if isinstance(level_manager.level, GameState):
            self.player = level_manager.level.player


    def update_animation(self, state="", invert=False,lock=False):
        self.update_state()
        Animation.update_animation(self)

    def update_state(self):
        self.state = 'still'
        self.obj.pos = physics_manager.get_body_position(self.obj.body)
