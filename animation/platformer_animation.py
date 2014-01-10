'''
Created on Sep 5, 2013

@author: efarhan
'''

import os
from os import listdir
from os.path import isfile, join
from engine.const import animation_step
from engine.event import get_keys
from Box2D import *
from physics.contact_listener import PlatformerContactListener
from physics.physics import pixel2meter
from engine.const import jump_step
from engine.const import invulnerability
import engine

class PlatformerAnimation():
    '''Manage the images and the animation of the demo-player'''
    def __init__(self, img_manager,size):
        self.img_manager = img_manager
        self.img = 0
        self.anim_counter = 0
        self.size = size
        self.foot_num = 0
        self.jump = 1
        self.right_side = True
        self.physics = None
        self.move = 0
        self.foot_sensor_size = (15,0.1)
        self.invulnerability = 0
        self.electricity,self.fire = False,False
        self.life = 100
        self.already_jumped = False
        self.jumped = False
        self.jump_step = 0
        self.UP, self.RIGHT,self.LEFT,self.DOWN,self.ACTION = 0, 0, 0, 0, 0
    def load_images(self):
        jump_path = 'data/sprites/hero/jump'
        move_path = 'data/sprites/hero/move'
        still_path = 'data/sprites/hero/still'
        
        jump_files = [ os.path.join(jump_path, f) for f in listdir(jump_path) if (isfile(join(jump_path, f)) and f.find(".png") != -1) ]
        jump_files.sort()
        move_files = [ os.path.join(move_path, f) for f in listdir(move_path) if (isfile(join(move_path, f)) and f.find(".png") != -1) ]
        move_files.sort()
        still_files = [ os.path.join(still_path, f) for f in listdir(still_path) if (isfile(join(still_path, f)) and f.find(".png") != -1) ]
        still_files.sort()
        
        self.jump_img = []
        self.move_img = []
        self.still_img = []
        for img in jump_files:
            self.jump_img.append(self.img_manager.load_with_size(img, self.size))
        for img in move_files:
            self.move_img.append(self.img_manager.load_with_size(img, self.size))
        for img in still_files:
            self.still_img.append(self.img_manager.load_with_size(img, self.size))
        self.img = self.still_img[0]
    def loop(self,player):
        if(self.invulnerability > 0):

            self.invulnerability-=1
        if(self.electricity or self.fire):
            if(self.invulnerability == 0):
                self.life-=100
                self.invulnerability = invulnerability
        if(self.life <= 0):
            engine.level_manager.level.death()
        #check event
        (self.RIGHT, self.LEFT,self.UP,self.DOWN,self.ACTION) = get_keys()
                                
        # set animation and velocity
        if self.foot_num < 1 and self.jump:
            self.jumped = False
            if self.right_side:
                self.set_state('jump_right')
            else:
                self.set_state('jump_left')
        if not self.UP and self.foot_num >= 1 and not self.jumped:
            self.already_jumped = False
        if self.UP and self.jump:
            if(not self.already_jumped or self.foot_num < 1):
                if self.right_side:
                    self.set_state('jump_right')
                else:
                    self.set_state('jump_left') 
            if not self.already_jumped and not self.foot_num < 1:
                self.physics.jump(player)
                self.already_jumped = True
                self.jumped = True
                self.jump_step = jump_step
            if self.jump_step > 0:
                self.physics.jump(player)
                self.jump_step -= 1
            if self.already_jumped and not self.foot_num < 1 and not self.RIGHT and not self.LEFT:
                if self.right_side:
                    self.set_state('still_right')
                else:
                    self.set_state('still_left')
                self.physics.move(player,0)
        else:
            self.jump_step = 0
        if self.RIGHT and not self.LEFT:
            #animation
            if (((not self.UP or not self.jump) or self.already_jumped) and not self.jumped) and (self.foot_num>=1 or not self.jump):
                self.set_state('move_right')
                #move the player
            if self.move != -1:
                self.physics.move(player,1)
            else:
                self.physics.move(player,0)
            self.right_side = True
        if self.LEFT and not self.RIGHT:
                #move the player
            if (((not self.UP or not self.jump) or self.already_jumped) and not self.jumped) and (self.foot_num>=1 or not self.jump):
                self.set_state('move_left')
            if self.move != 1:
                self.physics.move(player,-1)
            else:
                self.physics.move(player,0)
            self.right_side = False
        if not self.RIGHT and not self.UP and not self.LEFT:
            if self.foot_num >= 1 or not self.jump:
                if self.right_side:
                    self.set_state('still_right')
                else:
                    self.set_state('still_left')
                #stop the player
            self.physics.move(player,0)
        if self.RIGHT and self.LEFT:
            self.physics.move(player,0)
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
        
        self.contact_listener = PlatformerContactListener()
        self.physics.world.contactListener = self.contact_listener
        
    def set_state(self,state):
        if(state == 'jump_right'):
            self.img = self.jump_img[0]
        elif(state == 'jump_left'):
            self.img = self.jump_img[1]
        elif(state == 'move_right'):
            if(self.anim_counter == animation_step):
                anim_index = [self.move_img[0],self.move_img[2],self.move_img[4]]
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
        elif(state == 'move_left'):
            if(self.anim_counter == animation_step):
                anim_index = [self.move_img[1],self.move_img[3],self.move_img[5]]
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
        elif(state == 'still_right'):
            self.img = self.still_img[0]
        elif(state == 'still_left'):
            self.img = self.still_img[1]
    def touch_electricity(self,state):
        if(state):
            self.electricity = True
            if(self.invulnerability <= 0):
                #remove life
                self.invulnerability = invulnerability
                self.life -= 100
        else:
            self.electricity = False
    def touch_fire(self,state):
        if(state):
            self.fire = True
            if(self.invulnerability <= 0):
                #remove life
                self.invulnerability = invulnerability
                self.life -=100
        else:
            self.fire = False
            
