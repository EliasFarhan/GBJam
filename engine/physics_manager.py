'''
Manages physics with Box2D
convert automatically from pixel to meters
'''
import math
from numbers import Number
from engine.const import CONST, log, enum
from engine.vector import Vector2
from event.physics_event import clear_physics_event, PhysicsEvent,\
    add_physics_event

def pixel2meter(pixels):
    if isinstance(pixels,Vector2) or isinstance(pixels, Number):
        return pixels/CONST.ratio
    elif isinstance(pixels, tuple) or isinstance(pixels,list):
        return pixels[0]/CONST.ratio, pixels[1]/CONST.ratio
    else:
        raise TypeError("pixel2meter takes Vector2, numbers or tuple2")

    return None


def meter2pixel(meter):
    if isinstance(meter, Vector2) or isinstance(meter, Number):
        return meter*CONST.ratio
    elif isinstance(meter, tuple) or isinstance(meter, list):
        return meter[0]*CONST.ratio,meter[1]*CONST.ratio
    else:
        raise TypeError("pixel2meter takes Vector2, numbers or tuple2")
    return None

BodyType = enum("static", "dynamic","kinematic")
MoveType = enum("direct_set","force","impulse")

class PhysicsManager():
    def __init__(self):
        self.worlds = []
        self.current_world = None
    def init_world(self):
        pass

    def remove_world(self,world):
        pass

    @staticmethod
    def add_body(self,pos):
        pass

    @staticmethod
    def remove_body(self,body):
        pass

    @staticmethod
    def add_box():
        pass

    @staticmethod
    def add_circle():
        pass

    def loop(self):
        clear_physics_event()

    def exit(self):
        pass

physics_manager = PhysicsManager()
if CONST.physics == 'b2':
    from b2_engine.b2_physics_manager import Box2DPhysicsManager
    physics_manager = Box2DPhysicsManager()
elif CONST.physics == 'cymunk':
    import cymunk
elif CONST.physics == 'pookoo':
    import pookoo

def set_ratio_pixel(new_ratio):
    ratio = new_ratio

"""
def get_body_position(body):
    if body:
        if CONST.physics == 'b2':
            pos = Vector2(body.position)
        elif CONST.physics == 'pookoo':
            pos = Vector2(body.get_position())
        return meter2pixel(pos)
    else:
        return None


def set_body_position(body,pos):
    if body:
        body.position = pixel2meter(pos).get_tuple()


def deinit_physics():
    global world
    if CONST.physics != "pookoo":
        del world
    elif CONST.physics == 'pookoo':
        del world
    world = None


def init_physics(gravity_arg=None):
    global world
    log("Init world physics")
    if world != None:
        deinit_physics()

    gravity_value = Vector2(0,0)
    if(gravity_arg is None):
        gravity_value = Vector2(0,CONST.gravity)
    else:
        gravity_value = gravity_arg
    if CONST.physics == 'b2':
        pass
    elif CONST.physics == 'pookoo':
        log(gravity_value.get_tuple())
        world = pookoo.physics.World(gravity_value.get_float_tuple(), vel_iters, pos_iters)
    elif CONST.physics == 'cymunk':
        #world = cymunk.Space()
        pass


def add_dynamic_object(obj,pos):
    global world
    position = pixel2meter(pos)
    dynamic_object = None
    if CONST.physics == 'b2':
        dynamic_object = world.CreateDynamicBody(position=position.get_tuple())
        dynamic_object.angle = 0
        dynamic_object.fixed_rotation = True
    elif CONST.physics == 'pookoo':
        dynamic_object = pookoo.physics.Body(world,position.get_float_tuple(),'dynamic')
    elif CONST.physics == 'cymunk':
        pass
    return dynamic_object


def add_static_object(obj, pos):
    global world
    position = pixel2meter(pos)
    static_object = None
    if CONST.physics == 'b2':
        static_object = world.CreateStaticBody(position=position.get_float_tuple())
        static_object.angle = 0
        static_object.fixed_rotation = True
    elif CONST.physics == 'pookoo':
        static_object = pookoo.physics.Body(world,position.get_float_tuple(),'static')
    elif CONST.physics == 'cymunk':
        pass
    return static_object


def remove_body(index):
    try:
        world.DestroyBody(index)
    except KeyError:
        pass


def update_physics():
    clear_physics_event()
    if CONST.physics == 'b2':
        world.Step(timeStep,vel_iters,pos_iters)
        world.ClearForces()
    elif CONST.physics == 'pookoo':
        world.step(timeStep)


def move(body,vx=None,vy=None,linear=False):
    if CONST.physics == 'b2':
        if body:
            if not linear:
                dyn_obj = body

                velx,vely = dyn_obj.linearVelocity.x,dyn_obj.linearVelocity.y
                fx,fy=0,0
                if(vx != None):
                    velx = vx * CONST.move_speed - velx
                    fx = dyn_obj.mass * velx / timeStep
                if(vy != None):
                    vely = vy * CONST.move_speed - vely
                    fy = dyn_obj.mass * vely / timeStep
                if b2_module.__version__[0:3] == '2.3':
                    dyn_obj.ApplyForce(b2Vec2(fx,fy),dyn_obj.worldCenter,1)
                elif b2_module.__version__[0:3] == '2.1':
                    dyn_obj.ApplyForce(b2Vec2(fx,fy),dyn_obj.worldCenter)

            else:
                dyn_obj = body
                pos = dyn_obj.position
                dyn_obj.position = b2Vec2(pos[0]+vx*timeStep,pos[1]+vy*timeStep)


def jump(dyn_obj):
    force = dyn_obj.mass * jump / timeStep
    force /= float(CONST.jump_step)
    dyn_obj.ApplyForce(b2.Vec2(0,force),dyn_obj.worldCenter,True)


def add_static_box(body, pos, size, angle=0,data=0,sensor=False):
    if not (body and pos and size):
        log("Invalid arg body pos size in box creation",1)
        return None
    center_pos = pixel2meter(pos)
    if CONST.render != 'pookoo':
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(size.x), pixel2meter(size.y),
                               b2Vec2(center_pos.get_tuple()), angle*math.pi/180.0)
        fixture_def = b2FixtureDef()
        fixture_def.density = 1
        fixture_def.shape = polygon_shape

        fixture_def.userData = data
        fixture_def.isSensor = sensor
        return body.CreateFixture(fixture_def)
    elif CONST.render == 'pookoo':
        body.add_box(center_pos.get_tuple(),pixel2meter(size).get_tuple(),angle,sensor,data)


def add_static_circle(body,pos,radius,sensor=False,user_data=0):
    if not (body and pos and radius):
        log("Invalid arg body pos radius in circle creation",1)
        return None
    center_pos = pixel2meter(pos)

    circle_shape = b2CircleShape()
    circle_shape.pos = pixel2meter(pos).get_tuple()
    circle_shape.radius = pixel2meter(radius)

    fixture_def = b2FixtureDef()
    fixture_def.density = 1
    fixture_def.shape = circle_shape
    fixture_def.userData = user_data
    fixture_def.isSensor = sensor

    return body.CreateFixture(fixture_def)


def show_fixtures(screen,screen_pos,body):
    if CONST.physics == 'b2':
        body_pos = body.position
        body_pos = (meter2pixel(body_pos[0]), meter2pixel(body_pos[1]))

        for fixture in body.fixtures:
            fixture_pos = fixture.shape.vertices[0]
            fixture_pos = (meter2pixel(fixture_pos[0]),meter2pixel(fixture_pos[1]))
            fixture_pos = (body_pos[0]+fixture_pos[0],body_pos[1]+fixture_pos[1])
            fixture_size = [0.0,0.0]
            fixture_size = [fixture.shape.vertices[1][0]-fixture.shape.vertices[0][0],fixture.shape.vertices[2][1]-fixture.shape.vertices[0][1]]
            fixture_size = (fixture_size[0]/2, fixture_size[1]/2)
            fixture_size = (meter2pixel(fixture_size[0]),meter2pixel(fixture_size[1]))
            fixture_pos = (fixture_pos[0]+fixture_size[0],fixture_pos[1]+fixture_size[1])
            fixture_size = (2*fixture_size[0],2*fixture_size[1])
            rect = Rect(Vector2(fixture_pos),Vector2(fixture_size))
            rect.set_center(Vector2(fixture_pos))

            color = (255,0,0,200)
            if fixture.sensor == 1:
                color = (0,0,255,200)
            img_manager.draw_rect(screen, screen_pos, rect, color)
"""