from Box2D import *
import pygame

ratio = 64/1.5
def pixel2meter(pixels):
    global ratio
    return pixels/ratio
def meter2pixel(meter):
    global ratio
    return meter*ratio

class Physics():
    
    def __init__(self):
        self.world=b2World(gravity=(0,-10), doSleep=True)
    def init(self, static_objects, dynamic_objects):
        self.static_objects = {}
        self.dynamic_objects = {}
        for obj in static_objects:
            static_body = self.world.CreateStaticBody(\
                                position=(pixel2meter(obj.pos[0]), pixel2meter(obj.pos[1])),\
                                shapes=b2PolygonShape(box = (pixel2meter(obj.size[0]/2.0), pixel2meter(obj.size[1]/2.0))),\
                                                      )
            self.static_objects[obj] = static_body                                     
        for obj in dynamic_objects:
            dynamic_object = self.world.CreateDynamicBody(\
                                            position=(pixel2meter(obj.pos[0]), pixel2meter(obj.pos[1]))\
                                            )
            
            box = dynamic_object.CreatePolygonFixture(box = (pixel2meter(obj.size[0]/2.0), pixel2meter(obj.size[1]/2.0)), density=1,friction=0.3)
            self.dynamic_objects[obj] = dynamic_object
        self.timeStep = 1.0 / 30
        self.vel_iters, self.pos_iters = 10,10
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
        vel_change = value - vel
        force = dyn_obj.mass * vel_change / (1/30.0)
        dyn_obj.ApplyForce(b2Vec2(force,0),dyn_obj.worldCenter,True)
    def set_angle(self,obj,value):
        self.dynamic_objects[obj].angle = value
        self.dynamic_objects[obj].fixedRotation = True
    def jump(self,obj,value):
        pass