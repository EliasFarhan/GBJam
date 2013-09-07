from Box2D import *
import pygame
import engine

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
    def init(self):
        self.world=b2World(gravity=(0,-10), doSleep=True)
        self.static_objects = {}
        self.dynamic_objects = {}
        self.timeStep = 1.0 / 30
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
        vel_change = value - vel
        force = dyn_obj.mass * vel_change / (1/30.0)
        dyn_obj.ApplyForce(b2Vec2(force,0),dyn_obj.worldCenter,True)

    def jump(self,obj,value):
        dyn_obj = self.dynamic_objects[obj]
        impulse = dyn_obj.mass * value
        dyn_obj.ApplyLinearImpulse(b2Vec2(0,impulse),dyn_obj.worldCenter,True)
    def add_static_box(self,pos,size):
        static_body = self.world.CreateStaticBody(\
                                position=(pixel2meter(pos[0]), pixel2meter(pos[1])),\
                                shapes=b2PolygonShape(box = (pixel2meter(size[0]/2.0), pixel2meter(size[1]/2.0))),\
                                                      )
        self.static_objects[self.index] = static_body
        self.index+=1
        return self.index - 1
class ContactListener(b2ContactListener):
    def BeginContact(self, contact):
        fixture_user_data = contact.fixtureA.userData
        fixture_user_data2 = contact.fixtureB.userData
        # feet is touching something
        if((fixture_user_data == 3 and fixture_user_data2 != 5)\
           or (fixture_user_data2 == 3 and fixture_user_data != 5)):
            
            engine.level_manager.level.player.foot_num += 1
          
        #electricity touch the player  
        if((fixture_user_data == 4 and fixture_user_data2 == 5)\
           or (fixture_user_data == 5 and fixture_user_data2 == 4)):
            engine.level_manager.level.player.touch_electricity(True)
            
    def EndContact(self, contact):
        fixture_user_data = contact.fixtureA.userData
        fixture_user_data2 = contact.fixtureB.userData
        if((fixture_user_data == 3 and fixture_user_data2 != 5)\
           or fixture_user_data2 == 3 and fixture_user_data != 5):
            # feet is touching something
            engine.level_manager.level.player.foot_num -= 1
        #electricity does no more touch the player  
        if((fixture_user_data == 4 and fixture_user_data2 == 5)\
           or (fixture_user_data == 5 and fixture_user_data2 == 4)):
            engine.level_manager.level.player.touch_electricity(False)