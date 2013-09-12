from Box2D import *

import pygame
import engine
from engine.const import move, jump, framerate,jump_step,gravity

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

class Physics():
    def init(self,gravity_arg=None):
        if(gravity_arg == None):
            self.world=b2World(gravity=(0,gravity), doSleep=True)
        else:
            self.world=b2World(gravity=(0,gravity_arg), doSleep=True)
        self.static_objects = {}
        self.dynamic_objects = {}
        self.timeStep = 1.0 / framerate
        self.vel_iters, self.pos_iters = 10,10
        self.index = 1
    def add_static_object(self,obj):
        static_body = self.world.CreateStaticBody(\
                                position=(pixel2meter(obj.pos[0]), pixel2meter(obj.pos[1])),\
                                shapes=b2PolygonShape(box = (pixel2meter(obj.size[0]/2.0), pixel2meter(obj.size[1]/2.0))),\
                                                      )
        self.static_objects[obj] = static_body
        return static_body
    def add_dynamic_object(self,obj):
        dynamic_object = self.world.CreateDynamicBody(\
                                            position=(pixel2meter(obj.pos[0]), pixel2meter(obj.pos[1]))\
                                            )
            
        self.dynamic_objects[obj] = dynamic_object
        return dynamic_object
    def loop(self):
        self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)
        self.world.ClearForces()
        for obj in self.dynamic_objects.iterkeys():
            pos = self.dynamic_objects[obj].position
            obj.pos = (meter2pixel(pos[0]), meter2pixel(pos[1]))
            #print obj, obj.pos
    def move(self,obj,value):
        dyn_obj = self.dynamic_objects[obj]
        vel = dyn_obj.linearVelocity.x
        vel_change = value * move - vel
        force = dyn_obj.mass * vel_change / self.timeStep
        dyn_obj.ApplyForce(b2Vec2(force,0),dyn_obj.worldCenter,True)

    def jump(self,obj):
        dyn_obj = self.dynamic_objects[obj]
        force = dyn_obj.mass * jump / self.timeStep
        force /= float(jump_step)
        dyn_obj.ApplyForce(b2Vec2(0,force),dyn_obj.worldCenter,True)
    def add_static_box(self,pos,size):
        static_body = self.world.CreateStaticBody(\
                                position=(pixel2meter(pos[0]), pixel2meter(pos[1])),\
                                shapes=b2PolygonShape(\
                                                      box = (pixel2meter(size[0]/2.0), pixel2meter(size[1]/2.0))),\
                                                      )
        self.static_objects[self.index] = static_body
        self.index+=1
        return self.index - 1
    def add_static_circle(self,pos,radius):
        static_body = self.world.CreateStaticBody(\
                                position=(pixel2meter(pos[0]), pixel2meter(pos[1])),\
                                shapes=b2CircleShape(radius=pixel2meter(radius),)\
                                                     )
        self.static_objects[self.index] = static_body
        self.index+=1
        return self.index - 1
