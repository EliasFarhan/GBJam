'''
Manages physics with Box2D
convert automatically from pixel to meters
'''
import math
from engine.const import move_speed, jump, framerate,jump_step,gravity, log
from event.physics_event import clear_physics_event, PhysicsEvent,\
    add_physics_event
from Box2D import *
from engine.rect import Rect
from engine.image_manager import draw_rect

ratio = 64/1.5

def pixel2meter(pixels):
    return pixels/ratio
def meter2pixel(meter):
    return meter*ratio
def set_ratio_pixel(new_ratio):
    ratio = new_ratio
    

timeStep = 1.0 / framerate
vel_iters, pos_iters = 10,10
index = 1
world = None

def get_body_position(body):
    if body:
        pos = body.position
        return (meter2pixel(pos[0]),meter2pixel(pos[1]))
    else:
        return None
def deinit_physics():
    global world
    del world
    world = None
def init_physics(gravity_arg=None):
    global world
    if world != None:
        deinit_physics()
    
    gravity_value = 0
    if(gravity_arg == None):
        gravity_value = gravity 
    else:
        gravity_value = gravity_arg

    world = b2World(gravity=(0,gravity_value))
    world.contactListener = KuduContactListener()

def add_dynamic_object(obj,pos):
    global world
    position = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    dynamic_object = world.CreateDynamicBody(position=position)
    dynamic_object.angle = 0
    dynamic_object.fixed_rotation = True
    
    return dynamic_object

def add_static_object(obj,pos):
    global world
    position = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    static_object = world.CreateStaticBody(position=position)
    static_object.angle = 0
    static_object.fixed_rotation = True
    
    return static_object

def remove_body(index):
    try:
        world.DestroyBody(index)
    except KeyError:
        pass
def update_physics():
    clear_physics_event()

    world.Step(timeStep,vel_iters,pos_iters)
    world.ClearForces()
    
def move(body,vx=None,vy=None):
    if body:
        dyn_obj = body
    
        velx,vely = dyn_obj.linearVelocity.x,dyn_obj.linearVelocity.y
        fx,fy=0,0
        if(vx != None):
            velx = vx * move_speed - velx
            fx = dyn_obj.mass * velx / timeStep
        if(vy != None):
            vely = vy * move_speed - vely
            fy = dyn_obj.mass * vely / timeStep
        dyn_obj.ApplyForce(b2Vec2(fx,fy),dyn_obj.worldCenter,1)
def jump(dyn_obj):
    force = dyn_obj.mass * jump / timeStep
    force /= float(jump_step)
    dyn_obj.ApplyForce(b2.Vec2(0,force),dyn_obj.worldCenter,True)
    
def add_static_box(body,pos,size,angle=0,data=0,sensor=False):
    if not (body and pos and size):
        log("Invalid arg body pos size in box creation",1)
        return None
    center_pos = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    
    polygon_shape = b2PolygonShape()
    polygon_shape.SetAsBox(pixel2meter(size[0]), pixel2meter(size[1]),
                                   b2Vec2(center_pos),angle*math.pi/180.0)
    fixture_def = b2FixtureDef()
    fixture_def.density = 1
    fixture_def.shape = polygon_shape
    fixture_def.userData = data
    fixture_def.isSensor = sensor
    return body.CreateFixture(fixture_def)


            
    

def add_static_circle(pos,radius,sensor=False,user_data=0):
    static_body = world.CreateStaticBody(\
                                position=(pixel2meter(pos[0]), pixel2meter(pos[1])),\
                                shapes=b2.Circle(radius=pixel2meter(radius),)\
                                                     )
    
    
    return static_body

class KuduContactListener(b2ContactListener):
    def BeginContact(self, contact):
        a = contact.fixtureA
        b = contact.fixtureB
        add_physics_event(PhysicsEvent(a,b,True))
    def EndContact(self, contact):
        a = contact.fixtureA
        b = contact.fixtureB
        add_physics_event(PhysicsEvent(a,b,False))

def show_fixtures(screen,screen_pos,body):

    body_pos = body.position
    body_pos = (meter2pixel(body_pos[0]), meter2pixel(body_pos[1]))
    
    for fixture in body.fixtures:
        fixture_pos = fixture.shape.vertices[0]
        log(fixture.shape.vertices)
        fixture_pos = (meter2pixel(fixture_pos[0]),meter2pixel(fixture_pos[1]))
        fixture_pos = (body_pos[0]+fixture_pos[0],body_pos[1]+fixture_pos[1])
        fixture_size = [0.0,0.0]
        fixture_size = [fixture.shape.vertices[1][0]-fixture.shape.vertices[0][0],fixture.shape.vertices[2][1]-fixture.shape.vertices[0][1]]
        fixture_size = (fixture_size[0]/2, fixture_size[1]/2)
        fixture_size = (meter2pixel(fixture_size[0]),meter2pixel(fixture_size[1]))
        fixture_pos = (fixture_pos[0]+fixture_size[0],fixture_pos[1]+fixture_size[1])
        fixture_size = (2*fixture_size[0],2*fixture_size[1])
        rect = Rect(fixture_pos,fixture_size)
        rect.set_center(fixture_pos)

        color = (255,0,0,200)
        if fixture.sensor == 1:
            color = (0,0,255,200)
        draw_rect(screen, screen_pos, rect, color)