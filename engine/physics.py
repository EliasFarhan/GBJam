'''
Manages physics with Box2D
convert automatically from pixel to meters
'''
from engine.const import move_speed, jump, framerate,jump_step,gravity
from event.physics_event import clear_physics_event, PhysicsEvent,\
    add_physics_event
from Box2D import *

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

def deinit_physics():
    if pookoo:
        physics.close(world)
    else:
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
    position = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    dynamic_object = None
    if not pookoo:
        dynamic_object = world.CreateDynamicBody(position=position)
        dynamic_object.angle = 0
        dynamic_object.fixed_rotation = True
    else:
        dynamic_object = physics.body_add_dynamic(world,position[0],position[1])
    return dynamic_object

def remove_body(index):
    try:
        world.DestroyBody(index)
    except KeyError:
        pass
def update_physics():
    clear_physics_event()
    if not pookoo:
        world.Step(timeStep,vel_iters,pos_iters)
        world.ClearForces()
    else:
        physics.step(world,timeStep)
    
def move(body,vx=None,vy=None):
    dyn_obj = body
    if not pookoo:
        velx,vely = dyn_obj.linearVelocity.x,dyn_obj.linearVelocity.y
        fx,fy=0,0
        if(vx != None):
            velx = vx * move_speed - velx
            fx = dyn_obj.mass * velx / timeStep
        if(vy != None):
            vely = vy * move_speed - vely
            fy = dyn_obj.mass * vely / timeStep
        dyn_obj.ApplyForce(b2Vec2(fx,fy),dyn_obj.worldCenter,1)
def jump(obj):
    force = dyn_obj.mass * jump / timeStep
    force /= float(jump_step)
    dyn_obj.ApplyForce(b2.Vec2(0,force),dyn_obj.worldCenter,True)
    
def add_static_box(pos,size,angle=0,data=0,sensor=False,body=None):
    static_body = body
    if(static_body == None):
        pos_body = (pixel2meter(pos[0]), pixel2meter(pos[1]))
        if pookoo:
            static_body = physics.body_add_static(world,pos[0],pos[1])
            return static_body
        else:
            static_body = world.CreateStaticBody(position=pos_body)
            static_body.angle = 0
    
    center_pos = (0,0)
    if body != None:
        center_pos = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    if not pookoo:
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(size[0]), pixel2meter(size[1]),
                                   b2Vec2(center_pos),angle)
        fixture_def = b2FixtureDef()
        fixture_def.density = 1
        fixture_def.shape = polygon_shape
        fixture_def.userData = data
        fixture_def.isSensor = sensor
        static_body.CreateFixture(fixture_def)
        
        if body == None:
            return static_body
    else:
        physics.geometry_add_box(static_body, 
                                 center_pos[0], center_pos[1],
                                 pixel2meter(size[0]),pixel2meter(size[1]),
                                 angle, sensor,
                                 data)
        if body == None:
            return static_body
            
    

def add_static_circle(pos,radius,sensor=False,user_data=0):
    static_body = world.CreateStaticBody(\
                                position=(pixel2meter(pos[0]), pixel2meter(pos[1])),\
                                shapes=b2.Circle(radius=pixel2meter(radius),)\
                                                     )
    static_objects[index] = static_body
    index+=1
    return index - 1

class KuduContactListener(b2ContactListener):
    def BeginContact(self, contact):
        a = contact.fixtureA.userData
        b = contact.fixtureB.userData
        add_physics_event(PhysicsEvent(a,b,True))
    def EndContact(self, contact):
        a = contact.fixtureA.userData
        b = contact.fixtureB.userData
        add_physics_event(PhysicsEvent(a,b,False))

