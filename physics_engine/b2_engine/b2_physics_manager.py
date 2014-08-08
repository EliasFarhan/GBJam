import math

import Box2D as b2_module
from Box2D import *

from engine.const import CONST, log
from physics_engine.physics_manager import pixel2meter, BodyType, MoveType
from physics_engine.physics_manager import PhysicsManager, meter2pixel
from engine.vector import Vector2
from event.physics_event import add_physics_event, PhysicsEvent


__author__ = 'Elias'


class Box2DPhysicsManager(PhysicsManager):
    def __init__(self):
        PhysicsManager.__init__(self)
        self.time_step = 1.0/CONST.framerate
        self.vel_iters = 10
        self.pos_iters = 10

    def init_world(self, gravity_arg=None):
        gravity_value = Vector2(0,0)
        if(gravity_arg is None):
            gravity_value = Vector2(0,CONST.gravity)
        else:
            gravity_value = gravity_arg
        world = b2World(gravity=gravity_value.get_tuple())
        world.contactListener = KuduContactListener()
        self.worlds.append(world)
        self.current_world = world

    def remove_world(self,world):
        self.worlds.remove(world)
        if world == self.current_world:
            del world
            self.current_world = None

    @staticmethod
    def get_body_position(body):
        return meter2pixel(Vector2(body.position))

    @staticmethod
    def set_body_position(body,pos):
        if body:
            body.position = pixel2meter(pos).get_tuple()

    def cast_ray(self,callback,point1,point2):
        if not (point2.x-point1.x == 0 and point2.y-point1.y == 0):
            p1 = b2Vec2(pixel2meter(point1).get_tuple())
            p2 = b2Vec2(pixel2meter(point2).get_tuple())
            self.current_world.RayCast(callback,p1,p2)

    def add_body(self,pos,body_type,angle=0,fixed_rotation=True, mass=1):
        physic_position = pixel2meter(pos).get_float_tuple()
        if body_type == BodyType.static:
            body = self.current_world.CreateStaticBody(position=physic_position)
        elif body_type == BodyType.dynamic:
            body = self.current_world.CreateDynamicBody(position=physic_position)
        elif body_type == BodyType.kinematic:
            body = self.current_world.CreateKinematicBody(position=physic_position)
        body.angle = angle
        body.fixedRotation = True
        body.mass = mass
        return body

    @staticmethod
    def add_box(body, pos, size, angle=0,data=None,sensor=False,density=1):
        if not (body and pos and size):
            log("Invalid arg body pos size in box creation",1)
            return None
        center_pos = pixel2meter(pos)
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(size.x), pixel2meter(size.y),
                               b2Vec2(center_pos.get_tuple()), angle*math.pi/180.0)
        fixture_def = b2FixtureDef()
        fixture_def.density = density
        fixture_def.shape = polygon_shape

        fixture_def.userData = data
        fixture_def.isSensor = sensor
        return body.CreateFixture(fixture_def)

    @staticmethod
    def add_circle(body, pos, radius, sensor=False, data=None, density=1):
        if not (body and pos and radius):
            log("Invalid arg body pos radius in circle creation",1)
            return None
        center_pos = pixel2meter(pos)

        circle_shape = b2CircleShape()
        circle_shape.pos = pixel2meter(pos).get_tuple()
        circle_shape.radius = pixel2meter(radius)

        fixture_def = b2FixtureDef()
        fixture_def.density = density
        fixture_def.shape = circle_shape
        fixture_def.userData = data
        fixture_def.isSensor = sensor

        return body.CreateFixture(fixture_def)

    def remove_body(self,body):
        self.current_world.DestroyBody(body)

    def loop(self):
        PhysicsManager.loop(self)
        for world in self.worlds:
            world.Step(self.time_step,self.vel_iters,self.pos_iters)
            world.ClearForces()

    def move(self, body, vx=None, vy=None, movement_type=MoveType.force):
        if body:
            if movement_type == MoveType.force:
                dyn_obj = body

                velx, vely = dyn_obj.linearVelocity.x,dyn_obj.linearVelocity.y
                fx,fy=0,0
                if(vx != None):
                    velx = vx * CONST.move_speed - velx
                    fx = dyn_obj.mass * velx / self.time_step
                if(vy != None):
                    vely = vy * CONST.move_speed - vely
                    fy = dyn_obj.mass * vely / self.time_step
                if b2_module.__version__[0:3] == '2.3':
                    dyn_obj.ApplyForce(b2Vec2(fx,fy),dyn_obj.worldCenter,1)
                elif b2_module.__version__[0:3] == '2.1':
                    dyn_obj.ApplyForce(b2Vec2(fx,fy),dyn_obj.worldCenter)

            else:
                dyn_obj = body
                pos = dyn_obj.position
                if vx is not None:
                    dyn_obj.position = b2Vec2(pos[0]+vx*self.time_step,pos[1])
                if vy is not None:
                    dyn_obj.position = b2Vec2(pos[0],pos[1]+vy*self.time_step)

    def jump(self,dyn_obj, impulse=0):
        if impulse == 0:
            force = dyn_obj.mass * CONST.jump / self.time_step
            force /= float(CONST.jump_step)
            if b2_module.__version__[0:3] == '2.3':
                dyn_obj.ApplyForce(b2Vec2(0,-force),dyn_obj.worldCenter,True)
            elif b2_module.__version__[0:3] == '2.1':
                dyn_obj.ApplyForce(b2Vec2(0,-force),dyn_obj.worldCenter)
        elif impulse == 1:
            impulse = dyn_obj.mass * CONST.jump
            if b2_module.__version__[0:3] == '2.3':
                dyn_obj.ApplyLinearImpulse( b2Vec2(0,-impulse), dyn_obj.worldCenter,True )
            elif b2_module.__version__[0:3] == '2.1':
                dyn_obj.ApplyLinearImpulse( b2Vec2(0,-impulse), dyn_obj.worldCenter)
    def exit(self):
        for world in self.worlds:
            world.__swig_destroy__()
            del world
        del self.worlds

    def get_body_velocity(self, body):
        return Vector2(body.linearVelocity)

    def set_body_velocity(self,body,new_v):
        body.linearVelocity = b2Vec2(new_v.x, new_v.y)

class KuduContactListener(b2ContactListener):
    def BeginContact(self, contact):
        a = contact.fixtureA
        b = contact.fixtureB
        add_physics_event(PhysicsEvent(a, b, True))
    def EndContact(self, contact):
        a = contact.fixtureA
        b = contact.fixtureB
        add_physics_event(PhysicsEvent(a, b, False))


class RayCastClosestCallback(b2RayCastCallback):
    """This callback finds the closest hit"""
    def __repr__(self): return 'Closest hit'
    def __init__(self, **kwargs):
        b2RayCastCallback.__init__(self, **kwargs)
        self.fixture=None
        self.hit=False
        self.fraction = 1.0
    # Called for each fixture found in the query. You control how the ray proceeds
    # by returning a float that indicates the fractional length of the ray. By returning
    # 0, you set the ray length to zero. By returning the current fraction, you proceed
    # to find the closest point. By returning 1, you continue with the original ray
    # clipping. By returning -1, you will filter out the current fixture (the ray
    # will not hit it).

    def ReportFixture(self, fixture, point, normal, fraction):
        self.hit=True
        self.fixture=fixture
        self.point=b2Vec2(point)
        self.normal=b2Vec2(normal)
        self.fraction = fraction
        return self.fraction