'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object import GameObject
import pygame
from Box2D import *
from physics.physics import pixel2meter
from engine.const import animation_step
from engine.image_manager import rot_center,rot_electricity
from math import radians

class Electricity(GameObject):
    def __init__(self, pos_a, physics,vertical=False,turning=0):
        GameObject.__init__(self, physics)
        self.turning = turning
        self.img = []
        self.size = (128,32)
        self.pos = pos_a
        self.anim_counter = 0
        self.vertical = vertical
        self.angle = 0
        if self.vertical:
            self.angle = 90
        self.line_index = 1
        self.load_images()
        self.init_physics()
    def load_images(self):
        path = 'data/sprites/electricity/'
        base = None
        if self.turning == 0:
            base = path+'box.png'
        else:
            base = path+'ball.png'
        line1 = path+'line1.png'
        line2 = path+'line2.png'
        self.img.append(self.img_manager.load_with_size(base, (self.size[1],self.size[1])))
        self.img.append(self.img_manager.load_with_size(line1, self.size))
        self.img.append(self.img_manager.load_with_size(line2, self.size))            
    def loop(self,screen,screen_pos):
        
        if(self.anim_counter == animation_step):
            if self.line_index == 1:
                self.line_index = 2
            else:
                self.line_index = 1
                self.anim_counter = 0
        else:
            self.anim_counter += 1
        if self.turning != 0:
            #turn everything
            self.box.angle = radians(self.angle)
            self.angle += self.turning
            self.img_manager.show(self.img[self.line_index],screen,(self.pos[0]+self.size[0]/2-screen_pos[0],self.pos[1]-screen_pos[1]),self.angle,rot_electricity)
        else:
            if(not self.vertical):
                self.img_manager.show(self.img[self.line_index],screen,(self.pos[0]+self.size[0]/2+self.size[1]/2-screen_pos[0],self.pos[1]-screen_pos[1]))
                self.img_manager.show(self.img[0],screen,(self.pos[0]+self.size[0]+self.size[1]-screen_pos[0],self.pos[1]-screen_pos[1]))
            else:
                self.img_manager.show(self.img[self.line_index],screen,(self.pos[0]-screen_pos[0],self.pos[1]+self.size[0]/2+self.size[1]/2-screen_pos[1]),self.angle,rot_center)
                self.img_manager.show(self.img[0],screen,(self.pos[0]-screen_pos[0],self.pos[1]+self.size[0]+self.size[1]-screen_pos[1]))
        self.img_manager.show(self.img[0], screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]))
    def init_physics(self):
        pos_box1 = self.pos
        index = 0
        if self.turning == 0:
            index = self.physics.add_static_box(pos_box1, (self.size[1],self.size[1]))
        else:
            index = self.physics.add_static_circle(pos_box1,12)
        self.box = self.physics.static_objects[index]
        
        pos_box2 = (self.size[0]+self.size[1],0)
        
        
        if(self.turning == 0):
            #add other box
            
            polygon_shape = b2PolygonShape()
            if(self.vertical):
                polygon_shape.SetAsBox(pixel2meter(self.size[1]/2.0),pixel2meter(self.size[1]/2.0),b2Vec2(pixel2meter(pos_box2[1]),pixel2meter(pos_box2[0])),0)
            else:
                polygon_shape.SetAsBox(pixel2meter(self.size[1]/2.0),pixel2meter(self.size[1]/2.0),b2Vec2(pixel2meter(pos_box2[0]),pixel2meter(pos_box2[1])),0)
            fixture_def = b2FixtureDef()
            fixture_def.shape = polygon_shape
            fixture_def.density = 1
            self.box.CreateFixture(fixture_def)
        
        #add electricity sensor
        size = ()
        if not self.vertical:
            pos_box2 = (self.size[1]/2.0+self.size[0]/2.0,0)
            size = (self.size[0],self.size[1]-10)
        else:
            pos_box2 = (0,self.size[1]/2.0+self.size[0]/2.0)
            size = (self.size[1]-10,self.size[0])
        if self.turning != 0:
            size = (size[0]-32, size[1])
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(size[0]/2.0),pixel2meter(size[1]/2.0),b2Vec2(pixel2meter(pos_box2[0]),pixel2meter(pos_box2[1])),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 0
        fixture_def.isSensor = True
        self.elec_sensor_fixture = self.box.CreateFixture(fixture_def)
        self.elec_sensor_fixture.userData = 5