from animation.animation_main import Animation
from engine.vector import Vector2
from extensions.animation.bullet_animation import BulletAnimation
from game_object.game_object_main import GameObject
from game_object.image import Image
from physics_engine.physics_manager import physics_manager, BodyType, MoveType

__author__ = 'Elias'

class Bullet(Image):
    def __init__(self,pos,size,userData=0,speed=Vector2(-5,0)):
        GameObject.__init__(self)
        self.pos = pos
        self.parallax_factor = 1.0
        self.size = size
        self.show = True
        self.flip = False
        self.body = physics_manager.add_body(self.pos+self.size/2,BodyType.dynamic)
        physics_manager.add_box(self.body,Vector2(),Vector2(self.size.x/2,2),data=userData,sensor=True)
        physics_manager.move(self.body,vx=-5)
        self.anim = BulletAnimation(self)