import pypybox2d as b2 

import pygame
import engine
from engine.const import move, jump, framerate,jump_step,gravity
from pypybox2d import world
from physics.contact_listener import KuduContactListener

ratio = 64/1.5

def pixel2meter(pixels):
    global ratio
    return pixels/ratio
def meter2pixel(meter):
    global ratio
    return meter*ratio
def set_ratio_pixel(new_ratio):
    global ratio
    ratio = new_ratio
    
static_objects = {}
dynamic_objects = {}
timeStep = 1.0 / framerate
vel_iters, pos_iters = 10,10
index = 1

def init_physics(gravity_arg=None):
    global world,static_objects,dynamic_objects
    if(gravity_arg == None):
        world= b2.World(gravity=(0,gravity))
    else:
        world=b2.World(gravity=(0,gravity_arg))
    
    world.contact_manager = KuduContactListener()
    
def add_static_object(obj,sensor=False,user_data=0):
    global world,static_objects
    if(obj.size[0] != 0 and obj.size[1]!= 0):
        static_body = world.CreateStaticBody(\
                                    position=(pixel2meter(obj.pos[0]), pixel2meter(obj.pos[1])),\
                                    shapes=b2.Polygon(box = (pixel2meter(obj.size[0]/2.0), pixel2meter(obj.size[1]/2.0))),\
                                                          )
        static_objects[obj] = static_body
        return static_body
    return None

def add_dynamic_object(obj,sensor=False,user_data=0):
    global world,dynamic_objects
    dynamic_object = world.CreateDynamicBody(\
                                            position=(pixel2meter(obj.pos[0]), pixel2meter(obj.pos[1]))\
                                            )
            
    dynamic_objects[obj] = dynamic_object
    return dynamic_object

def update_physics():
    world.ttep(timeStep, vel_iters, pos_iters)
    world.clear_forces()
    for obj in dynamic_objects.iterkeys():
        pos = dynamic_objects[obj].position
        obj.pos = (meter2pixel(pos[0]), meter2pixel(pos[1]))
            #print obj, obj.pos
            
def move(obj,vx=None,vy=None):
    dyn_obj = dynamic_objects[obj]
    velx,vely = dyn_obj.linearVelocity.x,dyn_obj.linearVelocity.y
    fx,fy=0,0
    if(vx != None):
        velx = vx * move - velx
        fx = dyn_obj.mass * velx / timeStep
    if(vy != None):
        vely = vy * move - vely
        fy = dyn_obj.mass * vely / timeStep
    dyn_obj.ApplyForce(b2.Vec2(fx,fy),dyn_obj.worldCenter,True)

def jump(obj):
    dyn_obj = dynamic_objects[obj]
    force = dyn_obj.mass * jump / timeStep
    force /= float(jump_step)
    dyn_obj.ApplyForce(b2.Vec2(0,force),dyn_obj.worldCenter,True)
    
def add_static_box(pos,size,angle=0,data=0,sensor=False):
    global world,static_objects,index
    static_body = b2.Body(world,(pixel2meter(pos[0]), pixel2meter(pos[1]))) 
                                
        
    static_body.angle = angle
    polygon_shape = b2.Polygon()
        
    polygon_shape.set_as_box(pixel2meter(size[0]/2.0), pixel2meter(size[1]/2.0))
    fixture_def = b2.Fixture(polygon_shape, friction=0, density=1, sensor=sensor, user_data=data, body=static_body)
    static_objects[index] = static_body
    index+=1
    return index - 1

def add_static_circle(pos,radius,sensor=False,user_data=0):
    static_body = world.CreateStaticBody(\
                                position=(pixel2meter(pos[0]), pixel2meter(pos[1])),\
                                shapes=b2.Circle(radius=pixel2meter(radius),)\
                                                     )
    static_objects[index] = static_body
    index+=1
    return index - 1

