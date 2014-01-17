import pypybox2d as b2 

import pygame
import engine
from engine.const import move_speed, jump, framerate,jump_step,gravity, log
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
timeStep = 1.0 / framerate
vel_iters, pos_iters = 10,10
index = 1
world = None

def init_physics(gravity_arg=None):
    global world,static_objects,dynamic_objects
    if(gravity_arg == None):
        world=b2.World(gravity=(0,gravity))
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

def add_dynamic_object(obj,pos):
    global world
    position = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    dynamic_object = world.create_dynamic_body(position=position)
    dynamic_object.angle = 0
    dynamic_object.fixed_rotation = True
    return dynamic_object

def update_physics():
    global timeStep, vel_iters, pos_iters
    world.step(timeStep, vel_iters, pos_iters)
    world.clear_forces()
    
def move(body,vx=None,vy=None):
    dyn_obj = body
    velx,vely = dyn_obj.linear_velocity.x,dyn_obj.linear_velocity.y
    fx,fy=0,0
    if(vx != None):
        velx = vx * move_speed - velx
        fx = dyn_obj.mass * velx / timeStep
    if(vy != None):
        vely = vy * move_speed - vely
        fy = dyn_obj.mass * vely / timeStep
    dyn_obj.apply_force(b2.Vec2(fx,fy),dyn_obj.world_center)

def jump(obj):
    dyn_obj = dynamic_objects[obj]
    force = dyn_obj.mass * jump / timeStep
    force /= float(jump_step)
    dyn_obj.ApplyForce(b2.Vec2(0,force),dyn_obj.worldCenter,True)
    
def add_static_box(pos,size,angle=0,data=0,sensor=False,body=None):
    global world,static_objects,index
    static_body = body
    if(static_body == None):
        static_body = world.create_static_body(position=(pixel2meter(pos[0]), pixel2meter(pos[1])))
        
        
    static_body.angle = angle
    polygon_shape = b2.Polygon()
    
    center_pos = (0,0)
    if body == None:
        center_pos = (pixel2meter(pos[0]),pixel2meter(pos[1]))
    polygon_shape.set_as_box(pixel2meter(size[0]/2.0), pixel2meter(size[1]/2.0),
                             center=center_pos)
    fixture_def = static_body.create_fixture(polygon_shape, sensor=sensor, user_data=data)
    if body == None:
        log(static_body)
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

