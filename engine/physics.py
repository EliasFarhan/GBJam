'''
Manages physics with Box2D
convert automatically from pixel to meters
'''
import math
from engine.const import CONST, log
from event.physics_event import clear_physics_event, PhysicsEvent,\
    add_physics_event

if CONST.physics == 'b2':
    import Box2D as b2_module
    from Box2D import *
elif CONST.physics == 'cymunk':
    import cymunk
elif CONST.physics == 'pookoo':
    import pookoo
from engine.rect import Rect
from engine.image_manager import draw_rect
from numbers import Number
from engine.vector import Vector2


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


def set_ratio_pixel(new_ratio):
    ratio = new_ratio


timeStep = 1.0 / CONST.framerate
vel_iters, pos_iters = 10,10
index = 1
world = None


def get_body_position(body):
    if body:
        pos = Vector2(body.position)
        return meter2pixel(pos)
    else:
        return None


def set_body_position(body,pos):
    if body:
        body.position = pixel2meter(pos).get_tuple()


def deinit_physics():
    global world
    if CONST.render != "pookoo":
        del world
    elif CONST.render == 'pookoo':
        pookoo.physics.finish(world)
    world = None


def init_physics(gravity_arg=None):
    global world
    if world != None:
        deinit_physics()

    gravity_value = Vector2(0,0)
    if(gravity_arg == None):
        gravity_value = Vector2(0,CONST.gravity)
    else:
        gravity_value = gravity_arg
    if CONST.physics == 'b2':
        world = b2World(gravity=gravity_value.get_tuple())
        world.contactListener = KuduContactListener()
    elif CONST.physics == 'pookoo':
        world = pookoo.physics.begin(gravity_value.get_tuple())
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
        dynamic_object = pookoo.physics.Body(pos.get_tuple())
    elif CONST.physics == 'cymunk':
        pass
    return dynamic_object


def add_static_object(obj, pos):
    global world
    position = pixel2meter(pos)
    static_object = None
    if CONST.physics == 'b2':
        static_object = world.CreateStaticBody(position=position.get_tuple())
        static_object.angle = 0
        static_object.fixed_rotation = True
    elif CONST.physics == 'pookoo':
        static_object = pookoo.physics.body_add_static(world,pos.x,pos.y)
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


def move(body,vx=None,vy=None,linear=False):
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
        return None



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

if CONST.physics == 'b2':
    class KuduContactListener(b2ContactListener):
        def BeginContact(self, contact):
            a = contact.fixtureA
            b = contact.fixtureB
            add_physics_event(PhysicsEvent(a,b,True))
        def EndContact(self, contact):
            a = contact.fixtureA
            b = contact.fixtureB
            add_physics_event(PhysicsEvent(a,b,False))


def cast_ray(callback,point1,point2):
    if not (point2.x-point1.x == 0 and point2.y-point1.y == 0):
        p1 = b2Vec2(pixel2meter(point1).get_tuple())
        p2 = b2Vec2(pixel2meter(point2).get_tuple())
        world.RayCast(callback,p1,p2)

if CONST.render == 'b2':
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


def show_fixtures(screen,screen_pos,body):

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
        draw_rect(screen, screen_pos, rect, color)
