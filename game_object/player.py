'''
Created on 8 sept. 2013

@author: efarhan
'''
import pygame
import engine
from Box2D import *
from game_object import GameObject
from animation import DemoAnimation
from engine.event import get_keys
from engine.const import jump_step,invulnerability
from physics.physics import pixel2meter
from physics.contact_listener import ContactListener


class Player(GameObject):
    def __init__(self,physics,move=0,jump=1,factor=1):
        GameObject.__init__(self,physics)
        self.size = (64,64)
        self.box_size = (18,21)
        self.foot_sensor_size = (15,0.1)
        if(factor != 1):
            self.size = (factor*self.size[0],factor*self.size[1])
            self.box_size = (factor*self.box_size[0],factor*self.box_size[1])
            self.foot_sensor_size = (factor*self.foot_sensor_size[0],factor*self.foot_sensor_size[1])
        self.anim = DemoAnimation(self.img_manager,self.size)
        self.anim.load_images()
        self.move = move
        self.UP, self.RIGHT,self.LEFT,self.DOWN,self.ACTION = 0, 0, 0, 0, 0
        self.right_side = True
        self.init_physics()
        self.foot_num = 0
        self.jump = jump
        self.already_jumped = False
        self.jumped = False
        self.jump_step = 0
        self.invulnerablitiy = 0
        self.life = 100
        self.font = pygame.font.Font('data/font/8-BITWONDER.ttf',25)
        self.electricity,self.fire = False,False
    def loop(self, screen,screen_pos,new_size=1):
        #render life information
        msg_surface_obj = self.font.render('Life '+str(self.life), False, pygame.Color(255, 255, 255))
        msg_rect_obj = msg_surface_obj.get_rect()
        msg_rect_obj.topright = (screen.get_size()[0], 0)
        screen.blit(msg_surface_obj, msg_rect_obj)
        
        if(self.invulnerablitiy > 0):

            self.invulnerablitiy-=1
        if(self.electricity or self.fire):
            if(self.invulnerablitiy == 0):
                self.life-=100
                self.invulnerablitiy = invulnerability
        if(self.life <= 0):
            engine.level_manager.level.death()
        #check event
        (self.RIGHT, self.LEFT,self.UP,self.DOWN,self.ACTION) = get_keys()
                                
        # set animation and velocity
        if self.foot_num < 1 and self.jump:
            self.jumped = False
            if self.right_side:
                self.anim.loop('jump_right')
            else:
                self.anim.loop('jump_left')
        if not self.UP and self.foot_num >= 1 and not self.jumped:
            self.already_jumped = False
        if self.UP and self.jump:
            if(not self.already_jumped or self.foot_num < 1):
                if self.right_side:
                    self.anim.loop('jump_right')
                else:
                    self.anim.loop('jump_left') 
            if not self.already_jumped and not self.foot_num < 1:
                self.physics.jump(self)
                self.already_jumped = True
                self.jumped = True
                self.jump_step = jump_step
            if self.jump_step > 0:
                self.physics.jump(self)
                self.jump_step -= 1
            if self.already_jumped and not self.foot_num < 1 and not self.RIGHT and not self.LEFT:
                if self.right_side:
                    self.anim.loop('still_right')
                else:
                    self.anim.loop('still_left')
                self.physics.move(self,0)
        else:
            self.jump_step = 0
        if self.RIGHT and not self.LEFT:
            #animation
            if (((not self.UP or not self.jump) or self.already_jumped) and not self.jumped) and (self.foot_num>=1 or not self.jump):
                self.anim.loop('move_right')
                #move the player
            if self.move != -1:
                self.physics.move(self,1)
            else:
                self.physics.move(self,0)
            self.right_side = True
        if self.LEFT and not self.RIGHT:
                #move the player
            if (((not self.UP or not self.jump) or self.already_jumped) and not self.jumped) and (self.foot_num>=1 or not self.jump):
                self.anim.loop('move_left')
            if self.move != 1:
                self.physics.move(self,-1)
            else:
                self.physics.move(self,0)
            self.right_side = False
        if not self.RIGHT and not self.UP and not self.LEFT:
            if self.foot_num >= 1 or not self.jump:
                if self.right_side:
                    self.anim.loop('still_right')
                else:
                    self.anim.loop('still_left')
                #stop the player
            self.physics.move(self,0)
        if self.RIGHT and self.LEFT:
            self.physics.move(self,0)
        # show the current img
        self.pos = (int(self.pos[0]), int(self.pos[1]))
        if(self.invulnerablitiy%2!= 1):
            self.img_manager.show(self.anim.img, screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]),factor=new_size)
        return self.pos
        
    def init_physics(self):
        self.body = self.physics.add_dynamic_object(self)
        self.box = self.body.CreatePolygonFixture(box = (pixel2meter(self.box_size[0]), pixel2meter(self.box_size[1])), density=1,friction=0)
        self.body.fixedRotation = True
        self.body.angle = 0
        #add foot sensor
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(self.foot_sensor_size[0]), self.foot_sensor_size[1], b2Vec2(0,pixel2meter(-self.box_size[1])),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.foot_sensor_fixture = self.body.CreateFixture(fixture_def)
        self.foot_sensor_fixture.userData = 3
        #add hitbox
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter(self.box_size[0]),pixel2meter(self.box_size[1]))
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.hitbox_sensor_fixture = self.body.CreateFixture(fixture_def)
        self.hitbox_sensor_fixture.userData = 4
        
        self.contact_listener = ContactListener()
        self.physics.world.contactListener = self.contact_listener

    def touch_electricity(self,state):
        if(state):
            self.electricity = True
            if(self.invulnerablitiy <= 0):
                #remove life
                self.invulnerablitiy = invulnerability
                self.life -= 100
        else:
            self.electricity = False
    def touch_fire(self,state):
        if(state):
            self.fire = True
            if(self.invulnerablitiy <= 0):
                #remove life
                self.invulnerablitiy = invulnerability
                self.life -=100
        else:
            self.fire = False
    def set_position(self,new_pos):
        self.pos = new_pos
        self.body.position = (pixel2meter(new_pos[0]),pixel2meter(new_pos[1]))
        