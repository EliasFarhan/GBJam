'''
Created on 25 aout 2013

@author: efarhan
'''
import pygame

from engine.image_manager import img_manager
from pygame.locals import *
import engine.level_manager
import physics.physics as physics
from Box2D import *
import animation
from engine.event import keys


class GameObject():
    def __init__(self,physics):
        self.img_manager = img_manager
        self.pos = (0, 0)
        self.size = (0, 0)
        self.physics = physics
    def loop(self,screen):
        pass
    def init_physics(self):
        self.physics.add_static_object(self)
    

class Player(GameObject):
    def __init__(self,screen_size,physics):
        GameObject.__init__(self,physics)
        self.size = (64,64)
        self.anim = animation.DemoAnimation(self.img_manager,self.size)
        self.anim.load_images()
        
        self.UP, self.RIGHT,self.LEFT,self.DOWN,self.ACTION = 0, 0, 0, 0, 0
        self.init_physics()
        self.foot_num = 0
        self.already_jumped = False
        self.jumped = False
        self.invulnerablitiy = 0
        self.life = 100
        self.font = pygame.font.Font('data/font/8-BITWONDER.ttf',25)
        self.electricity = False
    def loop(self, screen):

        #render life information
        msg_surface_obj = self.font.render('Life '+str(self.life), False, pygame.Color(255, 255, 255))
        msg_rect_obj = msg_surface_obj.get_rect()
        msg_rect_obj.topright = (screen.get_size()[0], 0)
        screen.blit(msg_surface_obj, msg_rect_obj)
        
        if(self.invulnerablitiy > 0):
            self.invulnerablitiy-=1
        if(self.electricity and self.invulnerablitiy == 0):
            self.life-=20
            self.invulnerablitiy = 30
        if(self.life <= 0):
            engine.level_manager.switch('gameplay')
        #check event
        (self.RIGHT, self.LEFT,self.UP,self.DOWN,self.ACTION) = keys()
                                
        # set animation and velocity
        if self.foot_num < 1:
            self.jumped = False
            self.anim.loop('jump')
        if not self.UP and self.foot_num >= 1 and not self.jumped:
            self.already_jumped = False
        if self.UP:
            if(not self.already_jumped or self.foot_num < 1):
                self.anim.loop('jump') 
            if not self.already_jumped and not self.foot_num < 1:
                self.physics.jump(self,7.5)
                self.already_jumped = True
                self.jumped = True
         
        if self.RIGHT:
            #animation
            if ((not self.UP or self.already_jumped) and not self.jumped) and self.foot_num>=1:
                self.anim.loop('move_right')
                #move the player
            self.physics.move(self,5)
        if self.LEFT:
                #move the player
            self.physics.move(self,-5)
                    
        if not self.RIGHT and not self.UP:
            if self.foot_num >= 1:
                self.anim.loop('still')
                #stop the player
            self.physics.move(self,0)
        # show the current img
        self.pos = (int(self.pos[0]), int(self.pos[1]))
        self.img_manager.show(self.anim.img, screen, (0,0))
        return self.pos
        
    def init_physics(self):
        dynamic_object = self.physics.add_dynamic_object(self)
        box = dynamic_object.CreatePolygonFixture(box = (physics.pixel2meter(20), physics.pixel2meter(20)), density=1,friction=0)
        dynamic_object.fixedRotation = True
        dynamic_object.angle = 0
        #add foot sensor
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(physics.pixel2meter(15), 0.1, b2Vec2(0,physics.pixel2meter(-20)),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.foot_sensor_fixture = dynamic_object.CreateFixture(fixture_def)
        self.foot_sensor_fixture.userData = 3
        #add hitbox
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(physics.pixel2meter(20),physics.pixel2meter(20))
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.hitbox_sensor_fixture = dynamic_object.CreateFixture(fixture_def)
        self.hitbox_sensor_fixture.userData = 4
        
        self.contact_listener = physics.ContactListener()
        self.physics.world.contactListener = self.contact_listener
    def touch_electricity(self,state):
        if(state):
            self.electricity = True
            if(self.invulnerablitiy <= 0):
                #remove life
                self.invulnerablitiy = 30
                self.life -= 20
        else:
            self.electricity = False
class Ground(GameObject):
    def __init__(self, screen_size,topleft_pos, nmb_block,physics):
        # set size
        GameObject.__init__(self,physics)
        self.block_size = (32,32)
        self.nmb_block = nmb_block
        self.size = (self.block_size[0]*self.nmb_block,self.block_size[1])
        self.rect = pygame.Rect(topleft_pos,self.size)
        self.pos = self.rect.center
        self.img = 0
        self.load_images()
        self.init_physics()
    def load_images(self):
        #load block
        self.img = self.img_manager.load_with_size('data/sprites/block/block1.png', self.block_size)
    def loop(self,screen,screen_pos):
        for i in range(self.nmb_block):
            self.img_manager.show(self.img, screen, \
                    (\
                     self.rect.midleft[0]+self.block_size[0]/2+i*self.block_size[0]-screen_pos[0],\
                     self.pos[1]-screen_pos[1])\
                                  )

class Electricity(GameObject):
    def __init__(self, screen_size,pos_a, physics,vertical=False,angle=0):
        GameObject.__init__(self, physics)
        self.angle = angle
        self.img = []
        self.size = (128,32)
        self.pos = pos_a
        self.anim_counter = 0
        self.vertical = vertical
        self.line_index = 1
        self.load_images()
        self.init_physics()
    def load_images(self):
        path = 'data/sprites/electricity/'
        box = path+'box.png'
        line1 = path+'line1.png'
        line2 = path+'line2.png'
        self.img.append(self.img_manager.load_with_size(box, (self.size[1],self.size[1])))
        self.img.append(self.img_manager.load_with_size(line1, self.size))
        self.img.append(self.img_manager.load_with_size(line2, self.size))            
    def loop(self,screen,screen_pos):
        self.img_manager.show(self.img[0], screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]))
        if(self.anim_counter == 3):
            if self.line_index == 1:
                self.line_index = 2
            else:
                self.line_index = 1
                self.anim_counter = 0
        else:
            self.anim_counter += 1
        if(not self.vertical):
            self.img_manager.show(self.img[self.line_index],screen,(self.pos[0]+self.size[0]/2+self.size[1]/2-screen_pos[0],self.pos[1]-screen_pos[1]))
            self.img_manager.show(self.img[0],screen,(self.pos[0]+self.size[0]+self.size[1]-screen_pos[0],self.pos[1]-screen_pos[1]))
        else:
            self.img_manager.show(self.img[self.line_index],screen,(self.pos[0]+self.size[0]/2.0-self.size[1]/2.0-screen_pos[0],self.pos[1]+self.size[0]-screen_pos[1]),90)
            self.img_manager.show(self.img[0],screen,(self.pos[0]-screen_pos[0],self.pos[1]+self.size[0]+self.size[1]-screen_pos[1]))
    def init_physics(self):
        pos_box1 = self.pos
        index = self.physics.add_static_box(pos_box1, (self.size[1],self.size[1]))
        self.box = self.physics.static_objects[index]
        #add other box
        pos_box2 = ()
        if not self.vertical:
            pos_box2 = (self.size[0]+self.size[1],0)
        else:pos_box2 = (0,self.size[0]+self.size[1])
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(physics.pixel2meter(self.size[1]/2.0),physics.pixel2meter(self.size[1]/2.0),b2Vec2(physics.pixel2meter(pos_box2[0]),physics.pixel2meter(pos_box2[1])),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        self.box.CreateFixture(fixture_def)
        #add electricity sensor
        size = ()
        if not self.vertical:
            pos_box2 = (self.size[1]/2.0+self.size[0]/2.0,0)
            size = self.size
        else:
            pos_box2 = (0,self.size[1]/2.0+self.size[0]/2.0)
            size = (self.size[1],self.size[0])
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(physics.pixel2meter(size[0]/2.0),physics.pixel2meter(size[1]/2.0-2),b2Vec2(physics.pixel2meter(pos_box2[0]),physics.pixel2meter(pos_box2[1])),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.elec_sensor_fixture = self.box.CreateFixture(fixture_def)
        self.elec_sensor_fixture.userData = 5
        
class FireTube(GameObject):
    def __init__(self, screen_size,pos_a, physics,vertical=False,angle=0):
        GameObject.__init__(self, physics)
        self.angle = angle
        self.img = []
        self.size = (128,32)
        self.pos = pos_a
        self.anim_counter = 0
        self.vertical = vertical
        self.line_index = 1
        self.load_images()
        self.init_physics()
    def load_images(self):
        path = 'data/sprites/fire/'
        box = path+'box.png'
        firemid = path+'firemid.png'
        fire = path+'fire.png'
        self.img.append(self.img_manager.load_with_size(box, (self.size[1],self.size[1])))
        self.img.append(self.img_manager.load_with_size(firemid, self.size))
        self.img.append(self.img_manager.load_with_size(fire, self.size))             
    def loop(self,screen,screen_pos):
        self.img_manager.show(self.img[0], screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]))
        if(self.anim_counter == 3):
            if self.line_index == 1:
                self.line_index = 2
            else:
                self.line_index = 1
            self.anim_counter = 0
        else:
            self.anim_counter += 1
        self.img_manager.show(self.img[self.line_index],screen,(self.pos[0]+self.size[0]/2+self.size[1]/2-screen_pos[0],self.pos[1]-screen_pos[1]))
        self.img_manager.show(self.img[0],screen,(self.pos[0]+self.size[0]+self.size[1]-screen_pos[0],self.pos[1]-screen_pos[1]))
    def init_physics(self):
        pos_box1 = self.pos
        index = self.physics.add_static_box(pos_box1, (self.size[1],self.size[1]))
        self.box = self.physics.static_objects[index]
        #add other box
        pos_box2 = (self.size[0]+self.size[1],0)
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(physics.pixel2meter(self.size[1]/2.0),physics.pixel2meter(self.size[1]/2.0),b2Vec2(physics.pixel2meter(pos_box2[0]),physics.pixel2meter(pos_box2[1])),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        self.box.CreateFixture(fixture_def)
        #add electricity sensor
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(physics.pixel2meter(self.size[0]/2.0),physics.pixel2meter(self.size[1]/2.0-2),b2Vec2(physics.pixel2meter(self.size[1]/2.0+self.size[0]/2.0),physics.pixel2meter(0)),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.elec_sensor_fixture = self.box.CreateFixture(fixture_def)
        self.elec_sensor_fixture.userData = 5
