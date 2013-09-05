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
    def __init__(self,physics):
        GameObject.__init__(self,physics)
        self.size = (64,64)
        self.anim = animation.DemoAnimation(self.img_manager,self.size)
        self.anim.load_images()
        self.joystick = 0
        self.UP, self.RIGHT = 0, 0

        if pygame.joystick.get_count() != 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        self.init_physics()
        self.foot_num = 0
        self.already_jumped = False
        self.jumped = False
    def loop(self, screen):
        # check events (with joystick)
        for event in pygame.event.get(): 
            if (self.joystick != 0):
                if (event.type == JOYHATMOTION):
                    if (self.joystick.get_hat(0) == (0, 1)):
                        self.UP = 1
                    elif(self.joystick.get_hat(0) == (0, -1)):
                        # DOWN
                        pass
                    elif(self.joystick.get_hat(0) == (1, 0)):
                        self.RIGHT = 1
                    elif(self.joystick.get_hat(0) == (-1, 0)):
                        # LEFT
                        pass
                    elif(self.joystick.get_hat(0) == (0, 0)):
                        self.UP, self.RIGHT = 0, 0
                elif event.type == JOYAXISMOTION:
                    if(self.joystick.get_axis(0)>0.9):
                        self.RIGHT = 1
                    else:
                        self.RIGHT = 0
                elif event.type == JOYBUTTONDOWN:
                    if(self.joystick.get_button(1)):
                        self.UP = 1
                elif event.type == JOYBUTTONUP:
                    if(self.joystick.get_button(1)):
                        self.UP = 0
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_w:
                    self.UP = 1
                elif event.key == K_DOWN:
                    # DOWN
                    pass
                elif event.key == K_RIGHT or event.key == K_d:
                    self.RIGHT = 1
                elif event.key == K_LEFT:
                    # LEFT
                    pass
            if event.type == KEYUP:
                if event.key == K_UP or event.key == K_w:
                    self.UP = 0
                elif event.key == K_DOWN:
                    # DOWN
                    pass
                elif event.key == K_RIGHT or event.key == K_d:
                    self.RIGHT = 0
                elif event.key == K_LEFT:
                    # LEFT
                    pass
                elif event.key == K_ESCAPE:
                    from engine.loop import end as end
                    end()
                        
            if event.type == QUIT:
                from engine.loop import end as end
                end()
                                
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
                self.anim.loop('move')
                #move the player
            self.physics.move(self,5)
                    
        if not self.RIGHT and not self.UP:
            if self.foot_num >= 1:
                self.anim.loop('still')
                #stop the player
            self.physics.move(self,0)
        # show the current img
        self.pos = (int(self.pos[0]), int(self.pos[1]))
        self.img_manager.show(self.anim.img, screen, (0,0))
        engine.level_manager.level.screen_pos = self.pos
        
    def init_physics(self):
        dynamic_object = self.physics.add_dynamic_object(self)
        box = dynamic_object.CreatePolygonFixture(box = (physics.pixel2meter(20.0), physics.pixel2meter(20.0)), density=1,friction=0)
        dynamic_object.fixedRotation = True
        dynamic_object.angle = 0
        #add foot sensor
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(physics.pixel2meter(15), 0.1, b2Vec2(0,physics.pixel2meter(-20.0)),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 1
        fixture_def.isSensor = True
        self.foot_sensor_fixture = dynamic_object.CreateFixture(fixture_def)
        self.foot_sensor_fixture.userData = 3
        self.feet_contact_listener = physics.FeetContactListener()
        engine.level_manager.level.physics.world.contactListener = self.feet_contact_listener
if __name__ == '__main__':
    p = Player()
    p.load_images()
