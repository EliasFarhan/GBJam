'''
Created on 8 sept. 2013

@author: efarhan
'''
from game_object import GameObject
from Box2D import *
from physics.physics import pixel2meter,meter2pixel
from engine.const import animation_step
from Box2D.Box2D import b2CircleShape

class FireTube(GameObject):
    def __init__(self, pos_a, physics,length=1,vertical=True,angle=0,begin=1):
        GameObject.__init__(self, physics)
        self.angle = angle
        self.img = []
        self.size = (32,32)
        self.length = length
        self.pos = pos_a
        self.begin = begin
        self.up = not begin
        self.height_fire = self.size[1]*(self.length+1)
        self.pos_fire = (self.pos[0],self.pos[1]+self.height_fire*self.begin)
        self.anim_counter = 0
        self.vertical = vertical
        self.line_index = 1
        self.load_images()
        self.init_physics()
        
        self.speed_move = 2
        self.ttw_cont = 60
        self.time = 0
        
    def load_images(self):
        path = 'data/sprites/fire/'
        box = path+'box.png'
        self.img.append(self.img_manager.load_with_size(box, (self.size[1],self.size[1])))
        self.img.append(self.img_manager.load_with_size(path+'firemid.png', self.size))
        self.img.append(self.img_manager.load_with_size(path+'firemid2.png', self.size))
        self.img.append(self.img_manager.load_with_size(path+'firemid3.png', self.size))
        self.img.append(self.img_manager.load_with_size(path+'fire.png', self.size))
        self.img.append(self.img_manager.load_with_size(path+'fire2.png', self.size))
        self.img.append(self.img_manager.load_with_size(path+'fire3.png', self.size))             
    def loop(self,screen,screen_pos):
        #manage the position of the fire
        if(self.pos_fire[1] >= self.pos[1]+self.height_fire and self.up):
            self.time = self.ttw_cont
            self.up = False
        elif(self.pos_fire[1] >= self.pos[1]+self.height_fire and not self.up and self.time > 0):
            self.time-=1
        elif(self.pos_fire[1] <= self.pos[1] and not self.up):
            self.time = self.ttw_cont
            self.up = True
        elif(self.pos_fire[1] <= self.pos[1] and self.up and self.time >0):
            self.time-=1
        elif(not self.up and self.time == 0):
            self.pos_fire= (self.pos_fire[0],self.pos_fire[1]-self.speed_move)
            self.fire.transform=(b2Vec2(self.fire.position[0],self.fire.position[1]-pixel2meter(self.speed_move)),0)
        elif(self.up and self.time == 0):
            self.pos_fire= (self.pos_fire[0],self.pos_fire[1]+self.speed_move)
            self.fire.transform=(b2Vec2(self.fire.position[0],self.fire.position[1]+pixel2meter(self.speed_move)),0)
        
        self.loop_physics()
        if(self.anim_counter == animation_step):
            if self.line_index > 0 and self.line_index < 3:
                self.line_index += 1
            else:
                self.line_index = 1
            self.anim_counter = 0
        else:
            self.anim_counter += 1
        for i in range(self.length):
            self.img_manager.show(self.img[self.line_index],screen,\
                                  (self.pos_fire[0]-screen_pos[0],self.pos_fire[1]-(i+1)*self.size[1]-screen_pos[1]))
        self.img_manager.show(self.img[self.line_index+3],screen,(self.pos_fire[0]-screen_pos[0],self.pos_fire[1]-screen_pos[1]))
        self.img_manager.show(self.img[0], screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]))
    def init_physics(self):
        
        pos_box1 = self.pos
        index = self.physics.add_static_box(pos_box1, (self.size[1],self.size[1]))
        self.box = self.physics.static_objects[index]
        
        #add fire sensor
        self.fire = self.physics.world.CreateStaticBody(position=\
                                        (pixel2meter(self.pos_fire[0]),\
                                         pixel2meter(self.pos_fire[1]-self.length*self.size[1])))
        self.fire.fixedRotation = True
        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter((self.size[0]-2)/2.0),pixel2meter(self.size[1]*(self.length+1)/2.0),b2Vec2((0.0,pixel2meter(self.size[1]*(self.length+1)/2))),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 0
        fixture_def.isSensor = True
        self.fire_sensor_fixture = self.fire.CreateFixture(fixture_def)
        self.fire_sensor_fixture.userData = 6
    def loop_physics(self):

        polygon_shape = b2PolygonShape()
        polygon_shape.SetAsBox(pixel2meter((self.size[0]-2)/2.0),pixel2meter((self.pos_fire[1]-self.pos[1])/2.0),b2Vec2((0.0,pixel2meter((self.pos_fire[1]-self.pos[1])/2))),0)
        fixture_def = b2FixtureDef()
        fixture_def.shape = polygon_shape
        fixture_def.density = 0
        fixture_def.isSensor = True
        self.fire.DestroyFixture(self.fire_sensor_fixture)
        self.fire_sensor_fixture = self.fire.CreateFixture(fixture_def)
        self.fire_sensor_fixture.userData = 6
        
class FireBall(GameObject):
    def __init__(self,pos,physics,max_dist=0,speed=0):
        GameObject.__init__(self, physics)
        self.size = (32,32)
        self.pos = pos
        self.min_dist = self.pos[0]
        self.max_dist = max_dist
        if max_dist != 0 and (self.min_dist > self.max_dist):
            a = self.min_dist
            self.min_dist = self.max_dist
            self.max_dist = a
        self.images = []
        self.img_index = 0
        self.anim_counter = 0
        self.change = False
        self.speed = speed
        self.init_physics()
        self.load_images()
    def load_images(self):
        path = 'data/sprites/fire/'
        files = [path+'fire_enemy1.png',path+'fire_enemy2.png']
        for f in files:
            self.images.append(self.img_manager.load_with_size(f, self.size))
    def loop(self, screen,screen_pos):
        #move the object
        if self.max_dist != 0:
            if not self.change and (self.pos[0]<=self.min_dist or self.pos[0]>=self.max_dist):
                self.body.linearVelocity = b2Vec2(-self.body.linearVelocity[0],self.body.linearVelocity[1])
                self.change = True
            elif(self.pos[0]<self.max_dist or self.pos[1]>self.min_dist):
                self.change = False
            
        #update movement
        self.pos = (meter2pixel(self.body.position[0]),meter2pixel(self.body.position[1]))
        if(self.anim_counter == animation_step):
            if self.img_index == 0:
                self.img_index += 1
            else:
                self.img_index = 0
            self.anim_counter = 0
        else:
            self.anim_counter += 1
        
        self.img_manager.show(self.images[self.img_index], screen, (self.pos[0]-screen_pos[0],self.pos[1]-screen_pos[1]))
    def init_physics(self):
        self.body = self.physics.world.CreateDynamicBody(position=b2Vec2(
                                                                         pixel2meter(self.pos[0]),
                                                                         pixel2meter(self.pos[1])))
        self.physics.dynamic_objects[self] = self.body
        circle_shape = b2CircleShape(radius=pixel2meter(self.size[1]/2))
        self.circle_fixture = self.body.CreateFixturesFromShapes(shapes=circle_shape)
        self.circle_fixture.friction=0
        self.circle_fixture.restitution=1
        self.circle_fixture.userData=6
        self.body.linearVelocity = b2Vec2(self.speed,0)