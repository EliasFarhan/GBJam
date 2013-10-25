'''
Created on 23 oct. 2013

@author: efarhan
'''
import os
from os import listdir
from os.path import isfile, join
from engine.event import get_keys

from engine.const import move,animation_step
from physics.physics import pixel2meter
from Box2D import *
from physics.contact_listener import RPGContactListener
class RPGAnimation():
    def __init__(self,img_manager,size):
        self.img_manager = img_manager
        self.img = 0
        self.anim_counter = 0
        self.size = size
        self.direction = True
        self.invulnerability = 0
        self.physics = None
    def load_images(self):
        img_path = 'data/sprites/rpg_move'
        
        img_files = [ os.path.join(img_path, f) for f in listdir(img_path) if (isfile(join(img_path, f)) and f.find(".png") != -1) ]
        img_files.sort()

        self.move_img = []
        for img in img_files:
            self.move_img.append(self.img_manager.load_with_size(img, self.size))

        self.img = self.move_img[4]
    def loop(self,player):
        
        #check event
        (self.RIGHT, self.LEFT,self.UP,self.DOWN,self.ACTION) = get_keys()
        
        horizontal, vertical = self.RIGHT-self.LEFT, self.DOWN-self.UP
        
        #set direction and animation
        if(self.direction and horizontal == 0 and vertical != 0):
            self.direction = False
        if(not self.direction and horizontal != 0 and vertical == 0):
            self.direction = True
        if(self.direction):
            #move horizontally
            if(horizontal == 1):
                #move right
                self.set_animation('right')
                self.physics.move(player,vx=move,vy=0)
            elif(horizontal == -1):
                self.set_animation('left')
                self.physics.move(player,vx=-move,vy=0)
            else:
                self.physics.move(player,vx=0,vy=0)
        else:
            #move vertically
            if(vertical == 1):
                self.set_animation('down')
                self.physics.move(player,vy=-move,vx=0)
            elif(vertical == -1):
                self.set_animation('up')
                self.physics.move(player,vy=move,vx=0)
            else:
                self.physics.move(player,vx=0,vy=0)
        
    def set_animation(self,state):
        if(state == 'right'):
            if(self.anim_counter == animation_step):
                anim_index = [self.move_img[6],self.move_img[7]]
                try:
                    find_index = anim_index.index(self.img)
                    if find_index == len(anim_index)-1:
                        self.img = anim_index[0]
                    else:
                        self.img = anim_index[find_index+1]
                except ValueError:
                    self.img = anim_index[0]
                self.anim_counter = 0
            else:
                self.anim_counter += 1
        elif(state == 'left'):
            if(self.anim_counter == animation_step):
                anim_index = [self.move_img[4],self.move_img[5]]
                try:
                    find_index = anim_index.index(self.img)
                    if find_index == len(anim_index)-1:
                        self.img = anim_index[0]
                    else:
                        self.img = anim_index[find_index+1]
                except ValueError:
                    self.img = anim_index[0]
                self.anim_counter = 0
            else:
                self.anim_counter += 1
        elif(state == 'up'):
            if(self.anim_counter == animation_step):
                anim_index = [self.move_img[0],self.move_img[1]]
                try:
                    find_index = anim_index.index(self.img)
                    if find_index == len(anim_index)-1:
                        self.img = anim_index[0]
                    else:
                        self.img = anim_index[find_index+1]
                except ValueError:
                    self.img = anim_index[0]
                self.anim_counter = 0
            else:
                self.anim_counter += 1
        elif(state == 'down'):
            if(self.anim_counter == animation_step):
                anim_index = [self.move_img[2],self.move_img[3]]
                try:
                    find_index = anim_index.index(self.img)
                    if find_index == len(anim_index)-1:
                        self.img = anim_index[0]
                    else:
                        self.img = anim_index[find_index+1]
                except ValueError:
                    self.img = anim_index[0]
                self.anim_counter = 0
            else:
                self.anim_counter += 1
    def init_physics(self,player):
        self.body = self.physics.add_dynamic_object(player)
        self.box = self.body.CreatePolygonFixture(box = (pixel2meter(player.box_size[0]), pixel2meter(player.box_size[1])), density=1,friction=0)
        self.body.fixedRotation = True
        self.body.angle = 0
        #add foot sensor
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(self.foot_sensor_size[0]), self.foot_sensor_size[1], b2Vec2(0,pixel2meter(-player.box_size[1])),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.foot_sensor_fixture = self.body.CreateFixture(fixture_def)
        self.foot_sensor_fixture.userData = 3
        #add hitbox
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(player.box_size[0]),pixel2meter(player.box_size[1]))
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.hitbox_sensor_fixture = self.body.CreateFixture(fixture_def)
        self.hitbox_sensor_fixture.userData = 4
        
        self.contact_listener = RPGContactListener()
        self.physics.world.contactListener = self.contact_listener